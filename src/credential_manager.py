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
        self.vault_path = ".vaults"

        # Create vaults directory if it does not exist
        if not os.path.exists(self.vault_path):
            os.mkdir(self.vault_path)

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
    def create_credential_file(self, name, master_password):
        path = self.vault_path + "/" + name

        # Check if vault name already exists
        if os.path.exists(path):
            raise FileExistsError("Vault with that name already exists")
        
        # Check if a master password was entered
        if len(master_password) == 0:
            raise ValueError("Must provide a valid master password")
        
        self.credential_file = path
        self.salt = os.urandom(16)
        self.key = self._derive_key(master_password, self.salt)
        self.cipher = Fernet(self.key)

        # Write salt at top of file (base64 encoded) and vault header
        with open(self.credential_file, "w") as file:
            file.write(base64.b64encode(self.salt).decode() + "\n")
            
            header = "VAULT_HEADER"
            header_enc = self.cipher.encrypt(header.encode()).decode()
            file.write(header_enc + "\n")

    # Load vault file, derive key from password and salt, and decrypt contents if password is correct
    def load_credential_file(self, name, master_password):
        path = self.vault_path + "/" + name

        # Check if vault file exists
        if not os.path.exists(path):
            raise FileNotFoundError("No vault exists with that name")

        self.credential_file = path
        with open(self.credential_file, "r") as file:
            lines = file.readlines()

        # First line is the salt
        self.salt = base64.b64decode(lines[0].strip())
        self.key = self._derive_key(master_password, self.salt)
        self.cipher = Fernet(self.key)

        # Check if master password is correct by decrypting vault header
        try:
            self.cipher.decrypt(lines[1].strip().encode())

        except:
            raise ValueError("Invalid master password")

        # Process each stored credential
        for line in lines[2:]:
            label_enc, username_enc, password_enc, email_enc = line.strip().split(" ")

            try:
                label_dec = self.cipher.decrypt(label_enc.encode()).decode()
                username_dec = self.cipher.decrypt(username_enc.encode()).decode()
                password_dec = self.cipher.decrypt(password_enc.encode()).decode()
                email_dec = self.cipher.decrypt(email_enc.encode()).decode()
            except:
                raise ValueError("File may have been corrupted")

            self.credential_dict[label_dec] = {
                "username": username_dec,
                "password": password_dec,
                "email": email_dec
            }
    
    # Add new credentials
    def add_credentials(self, label, username, password, email):
        if self.key is None:
            raise ValueError("Vault is locked (no key derived)")
        
        # Check if any values are empty
        if len(label) == 0 or len(username) == 0 or len(password) == 0 or len(email) == 0:
            raise ValueError("One or more values is empty")
        
        # Check if label already exists
        if label in self.credential_dict:
            raise ValueError("Entry with that label already exists")

        # Add to in-memory dict
        self.credential_dict[label] = {
            "username": username,
            "password": password,
            "email": email
        }

        # Encrypt and append to file
        label_enc = self.cipher.encrypt(label.encode()).decode()
        username_enc = self.cipher.encrypt(username.encode()).decode()
        password_enc = self.cipher.encrypt(password.encode()).decode()
        email_enc = self.cipher.encrypt(email.encode()).decode()

        with open(self.credential_file, "a") as file:
            file.write(f"{label_enc} {username_enc} {password_enc} {email_enc}\n")

    def delete_credentials(self, label):
        if self.key is None:
            raise ValueError("Vault is locked (no key derived)")
        
        # Check if entry exists
        if label not in self.credential_dict:
            raise ValueError("Entry with that label does not exist")
        
        # Delete credentials from dictionary and vault file
        del self.credential_dict[label]

        with open(self.credential_file, "r") as file:
            lines = file.readlines()

        # Find line to delete
        line_to_delete = 3
        for line in lines[2:]:
            label_enc = line.strip().split(" ")[0]
            label_dec = self.cipher.decrypt(label_enc.encode()).decode()
            if label == label_dec:
                break

            line_to_delete += 1

        # Rewrite vault contents minus deleted line
        with open(self.credential_file, "w") as file:
            line_number = 1
            for line in lines:
                if line_number == line_to_delete:
                    line_number += 1
                    continue

                file.write(line)
                line_number += 1

    # Retrieve credentials by label from dictionary
    def get_credentials(self, label):
        return self.credential_dict.get(label)
    
    # Reset manager members back to default
    def reset(self):
        self.key = None
        self.cipher = None
        self.salt = None
        self.credential_file = None
        self.credential_dict = {}