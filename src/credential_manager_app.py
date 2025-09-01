import tkinter as tk
from credential_manager import CredentialManager
from credential_manager_gui import CredentialManagerGUI

class CredentialManagerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Credential Manager")
        self.window.geometry("900x750")
        self.window.minsize(800, 700)
        self.manager = CredentialManager()
        self.gui = CredentialManagerGUI(self.window, self.manager)

    def run(self):
        self.window.mainloop()
