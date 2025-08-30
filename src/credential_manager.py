import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

class CredentialManager:
    def __init__(self):
        self.key = None
        self.cipher = None
        self.salt = None
        self.iterations = 390_000
        self.credential_file = None
        self.credential_dict = {}

    # Derive a Fernet key from password and salt
    def _derive_key(self, password, salt):
        # Hashing device
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
        )

        # Use hash and salt to generate key from password
        raw = kdf.derive(password.encode())
        return base64.urlsafe_b64encode(raw)

    # Create a credential file with salt and optional initial values
    def create_credential_file(self, path, master_password, initial_values=None):
        self.credential_file = path
        self.salt = os.urandom(16)
        self.key = self._derive_key(master_password, self.salt)
        self.cipher = Fernet(self.key)

        # Write salt at top of file (base64 encoded) and vault header
        with open(path, "w") as file:
            file.write(base64.b64encode(self.salt).decode() + "\n")
            
            header = "VAULT_HEADER"
            header_enc = self.cipher.encrypt(header.encode()).decode()
            file.write(header_enc)

        # Add initial values if provided
        if initial_values:
            for label, creds in initial_values.items():
                self.add_credentials(label, creds["username"], creds["password"], creds["email"])

    # Load vault file, derive key from password and salt, and decrypt contents if password is correct
    def load_credential_file(self, path, master_password):
        self.credential_file = path
        with open(path, "r") as file:
            lines = file.readlines()

        # First line is the salt
        self.salt = base64.b64decode(lines[0].strip())
        self.key = self._derive_key(master_password, self.salt)
        self.cipher = Fernet(self.key)

        # Check if master password is correct by decrypting vault header
        try:
            self.cipher.decrypt(lines[1])

        except:
            raise ValueError("Invalid master password or corrupted file")

        # Process each stored credential
        for line in lines[2:]:
            label_enc, username_enc, password_enc, email_enc = line.strip().split(" ")

            try:
                label_dec = self.cipher.decrypt(label_enc.encode()).decode()
                username_dec = self.cipher.decrypt(username_enc.encode()).decode()
                password_dec = self.cipher.decrypt(password_enc.encode()).decode()
                email_dec = self.cipher.decrypt(email_enc.encode()).decode()
            except:
                raise ValueError("Invalid master password or corrupted file")

            self.credential_dict[label_dec] = {
                "username": username_dec,
                "password": password_dec,
                "email": email_dec
            }
    
    # Add new credentials
    def add_credentials(self, label, username, password, email):
        if self.key is None:
            raise ValueError("Vault is locked (no key derived)")

        # Add to in-memory dict
        self.credential_dict[label] = {
            "username": username,
            "password": password,
            "email": email
        }

        # Encrypt and append to file
        encrypter = Fernet(self.key)
        label_enc = encrypter.encrypt(label.encode()).decode()
        username_enc = encrypter.encrypt(username.encode()).decode()
        password_enc = encrypter.encrypt(password.encode()).decode()
        email_enc = encrypter.encrypt(email.encode()).decode()

        with open(self.credential_file, "a") as file:
            file.write(f"{label_enc} {username_enc} {password_enc} {email_enc}\n")

    # Retrieve credentials by label from dictionary
    def get_credentials(self, label):
        return self.credential_dict.get(label)
    
if __name__ == "__main__":
    cm = CredentialManager()
    try:
        cm.load_credential_file("school.vault", "Jan122006!RTA")
    except ValueError as ve:
        print(f"Error: {str(ve)}")