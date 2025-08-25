from cryptography.fernet import Fernet

class CredentialManager:
    def __init__(self):
        self.key = None
        self.credential_file = None
        self.credential_dict = {}

    # Creates a key for encrypting/decrypting
    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as file:
            file.write(self.key)

    # Loads an existing key from device
    def load_key(self, path):
        with open(path, 'rb') as file:
            self.key = file.read()

    # Create a credential file to store credential data
    def create_credential_file(self, path, initial_values=None):
        self.credential_file = path

        # Add initial credentials if given
        if initial_values is not None:
            for label, credentials in initial_values.items():
                self.add_credentials(label, credentials["username"], credentials["password"], credentials["email"])

    # Load an encrypted credential file and decrypt components into dictionary
    def load_credential_file(self, path):
        self.credential_file = path

        with open(path, 'r') as file:
            for line in file:
                # Get encrypted components
                label_enc, username_enc, password_enc, email_enc = line.split(" ")

                # Decrypt components
                decrypter = Fernet(self.key)
                label_dec = decrypter.decrypt(label_enc.encode()).decode()
                username_dec = decrypter.decrypt(username_enc.encode()).decode()
                password_dec = decrypter.decrypt(password_enc.encode()).decode()
                email_dec = decrypter.decrypt(email_enc.encode()).decode()

                # Store data in dictionary
                self.credential_dict[label_dec] = {
                    "username": username_dec,
                    "password": password_dec,
                    "email": email_dec
                }
    
    # Add new credentials
    def add_credentials(self, label, username, password, email):
        # Add credentials to dictionary
        self.credential_dict[label] = {
            "username": username,
            "password": password,
            "email": email
        }

        # Add credentials to file
        if self.credential_file is not None:
            with open(self.credential_file, 'a+') as file:

                # Encrypt credentials
                encrypter = Fernet(self.key)
                label_enc = encrypter.encrypt(label.encode()).decode()
                username_enc = encrypter.encrypt(username.encode()).decode()
                password_enc = encrypter.encrypt(password.encode()).decode()
                email_enc = encrypter.encrypt(email.encode()).decode()

                # Write encrypted credentials to file
                file.write(label_enc + " " + username_enc + " " + password_enc + " " + email_enc + "\n")

    # Retrieve credentials by label from dictionary
    def get_credentials(self, label):
        return self.credential_dict[label]