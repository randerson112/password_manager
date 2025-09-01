import tkinter as tk
from credential_manager import CredentialManager

class CredentialManagerGUI:
    def __init__(self):
        # Main window
        self.root = tk.Tk()
        self.root.title("Credential Manager")
        self.root.geometry("600x450")

        # Credential manager system
        self.manager = CredentialManager()

        # Frames
        self.start_frame = tk.Frame(self.root)
        self.new_vault_frame = tk.Frame(self.root)
        self.open_vault_frame = tk.Frame(self.root)
        self.vault_management_frame = tk.Frame(self.root)
        self.frames = [self.start_frame, self.new_vault_frame, self.open_vault_frame, self.vault_management_frame]

        # Starting frame
        self.create_start_frame()

    # Clears window and sets a new frame
    def set_frame(self, new_frame):
        for frame in self.frames:
            frame.pack_forget()

        new_frame.pack(fill="both", expand=True)

    # Builds the start frame UI elements
    def create_start_frame(self):
        self.set_frame(self.start_frame)

        # Destroy old widgets
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        start_center_frame = tk.LabelFrame(self.start_frame, text="Choose An Option", labelanchor="n", padx=30, pady=30)
        start_center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create nwe vault button
        new_vault_button = tk.Button(start_center_frame, text="New Vault", command=self.create_new_vault_frame)
        new_vault_button.pack(pady=10, ipadx=5, ipady=10)

        # Open existing vault button
        open_vault_button = tk.Button(start_center_frame, text="Open Vault", command=self.create_open_vault_frame)
        open_vault_button.pack(pady=10, ipadx=5, ipady=10)

    # Builds the new vault frame UI elements
    def create_new_vault_frame(self):
        self.set_frame(self.new_vault_frame)

        # Destroy old widgets
        for widget in self.new_vault_frame.winfo_children():
            widget.destroy()

        new_vault_center_frame = tk.LabelFrame(self.new_vault_frame, text="Create New Vault", labelanchor="n", padx=30, pady=30)
        new_vault_center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Vault name input
        tk.Label(new_vault_center_frame, text="Vault Name:").pack(anchor="w", pady=(0, 5))
        self.vault_name_entry = tk.Entry(new_vault_center_frame, width=30)
        self.vault_name_entry.pack(pady=(0, 10))

        # Master password input
        tk.Label(new_vault_center_frame, text="Master Password:").pack(anchor="w", pady=(0, 5))
        self.master_password_entry = tk.Entry(new_vault_center_frame, width=30, show="*")
        self.master_password_entry.pack(pady=(0, 15))

        # Create and Back buttons
        tk.Button(new_vault_center_frame, text="Create Vault").pack(pady=5, ipadx=5, ipady=5)
        tk.Button(new_vault_center_frame, text="Back", command=self.create_start_frame).pack(pady=5, ipadx=5, ipady=5)

    # Builds the open vault frame UI elements
    def create_open_vault_frame(self):
        self.set_frame(self.open_vault_frame)

        # Destroy old widgets
        for widget in self.open_vault_frame.winfo_children():
            widget.destroy()

        open_vault_center_frame = tk.LabelFrame(self.open_vault_frame, text="Open Existing Vault", labelanchor="n", padx=30, pady=30)
        open_vault_center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Vault name input
        tk.Label(open_vault_center_frame, text="Vault Name:").pack(anchor="w", pady=(0, 5))
        vault_name_entry = tk.Entry(open_vault_center_frame, width=30)
        vault_name_entry.pack(pady=(0, 10))

        # Master password input
        tk.Label(open_vault_center_frame, text="Master Password:").pack(anchor="w", pady=(0, 5))
        master_password_entry = tk.Entry(open_vault_center_frame, width=30, show="*")
        master_password_entry.pack(pady=(0, 15))

        # Open and Back buttons
        tk.Button(open_vault_center_frame, text="Open Vault").pack(pady=5, ipadx=5, ipady=5)
        tk.Button(open_vault_center_frame, text="Back", command=self.create_start_frame).pack(pady=5, ipadx=5, ipady=5)

if __name__ == "__main__":
    cmgui = CredentialManagerGUI()
    cmgui.root.mainloop()