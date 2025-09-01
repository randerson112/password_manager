import tkinter as tk
from tkinter import ttk
from credential_manager import CredentialManager

class CredentialManagerGUI:
    def __init__(self):
        # Main window
        self.root = tk.Tk()
        self.root.title("Credential Manager")
        self.root.geometry("900x750")

        # Credential manager system
        self.manager = CredentialManager()

        # Frames
        self.start_frame = tk.Frame(self.root)
        self.new_vault_frame = tk.Frame(self.root)
        self.open_vault_frame = tk.Frame(self.root)
        self.vault_management_frame = tk.Frame(self.root)
        self.frames = [self.start_frame, self.new_vault_frame, self.open_vault_frame, self.vault_management_frame]

        # Starting frame
        self.create_vault_management_frame()

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
        self.create_vault_name_entry = tk.Entry(new_vault_center_frame, width=30)
        self.create_vault_name_entry.pack(pady=(0, 10))

        # Master password input
        tk.Label(new_vault_center_frame, text="Master Password:").pack(anchor="w", pady=(0, 5))
        self.create_master_password_entry = tk.Entry(new_vault_center_frame, width=30, show="*")
        self.create_master_password_entry.pack(pady=(0, 15))

        # Create and Back buttons
        tk.Button(new_vault_center_frame, text="Create Vault", command=self.create_vault).pack(pady=5, ipadx=5, ipady=5)
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
        self.open_vault_name_entry = tk.Entry(open_vault_center_frame, width=30)
        self.open_vault_name_entry.pack(pady=(0, 10))

        # Master password input
        tk.Label(open_vault_center_frame, text="Master Password:").pack(anchor="w", pady=(0, 5))
        self.open_master_password_entry = tk.Entry(open_vault_center_frame, width=30, show="*")
        self.open_master_password_entry.pack(pady=(0, 15))

        # Open and Back buttons
        tk.Button(open_vault_center_frame, text="Open Vault", command=self.open_vault).pack(pady=5, ipadx=5, ipady=5)
        tk.Button(open_vault_center_frame, text="Back", command=self.create_start_frame).pack(pady=5, ipadx=5, ipady=5)

    # Builds the vault managment frame UI elements
    def create_vault_management_frame(self):
        self.set_frame(self.vault_management_frame)

        # Destroy old widgets
        for widget in self.vault_management_frame.winfo_children():
            widget.destroy()

        # Credentials list
        frame_list = tk.LabelFrame(self.vault_management_frame, text="Stored Credentials", padx=10, pady=10)
        frame_list.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_list, columns=("Label", "Username", "Password", "Email"), show="headings")
        self.tree.heading("Label", text="Label")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True)

        # Notebook for Add/Edit/Delete
        notebook = ttk.Notebook(self.vault_management_frame)
        notebook.pack(padx=10, pady=10, fill="x")

        # --- Add Tab ---
        frame_add = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(frame_add, text="Add")

        tk.Label(frame_add, text="Label:").grid(row=0, column=0, sticky="e")
        tk.Label(frame_add, text="Username:").grid(row=1, column=0, sticky="e")
        tk.Label(frame_add, text="Password:").grid(row=2, column=0, sticky="e")
        tk.Label(frame_add, text="Email:").grid(row=3, column=0, sticky="e")

        self.entry_label = tk.Entry(frame_add)
        self.entry_user = tk.Entry(frame_add)
        self.entry_pass = tk.Entry(frame_add, show="*")
        self.entry_email = tk.Entry(frame_add)

        self.entry_label.grid(row=0, column=1, padx=5, pady=2)
        self.entry_user.grid(row=1, column=1, padx=5, pady=2)
        self.entry_pass.grid(row=2, column=1, padx=5, pady=2)
        self.entry_email.grid(row=3, column=1, padx=5, pady=2)

        tk.Button(frame_add, text="Confirm", command=self.add_credential).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Edit Tab ---
        self.edit_frame = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(self.edit_frame, text="Edit")

        tk.Label(self.edit_frame, text="Label:").grid(row=0, column=0, sticky="e")
        self.edit_label_entry = tk.Entry(self.edit_frame)
        self.edit_label_entry.grid(row=0, column=1)

        tk.Button(self.edit_frame, text="Edit", command=self.load_edit_fields).grid(row=1, column=0, columnspan=2, pady=10)

        # Container for edit fields (hidden initially)
        self.edit_fields_frame = tk.Frame(self.edit_frame)
        self.edit_fields_frame.grid(row=0, column=2, rowspan=3, sticky="ew")
        self.edit_fields_frame.grid_remove()

        # Labels and Entries inside edit_fields_frame
        tk.Label(self.edit_fields_frame, text="Label:").grid(row=0, column=0, sticky="e")
        tk.Label(self.edit_fields_frame, text="Username:").grid(row=1, column=0, sticky="e")
        tk.Label(self.edit_fields_frame, text="Password:").grid(row=2, column=0, sticky="e")
        tk.Label(self.edit_fields_frame, text="Email:").grid(row=3, column=0, sticky="e")

        self.edit_entry_label = tk.Entry(self.edit_fields_frame)
        self.edit_entry_user = tk.Entry(self.edit_fields_frame)
        self.edit_entry_pass = tk.Entry(self.edit_fields_frame, show="*")
        self.edit_entry_email = tk.Entry(self.edit_fields_frame)

        self.edit_entry_label.grid(row=0, column=1, padx=5, pady=2)
        self.edit_entry_user.grid(row=1, column=1, padx=5, pady=2)
        self.edit_entry_pass.grid(row=2, column=1, padx=5, pady=2)
        self.edit_entry_email.grid(row=3, column=1, padx=5, pady=2)

        # Save changes button
        tk.Button(self.edit_fields_frame, text="Save Changes", command=self.edit_credential).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Delete Tab ---
        frame_delete = tk.Frame(notebook, padx=10, pady=10)
        notebook.add(frame_delete, text="Delete")

        tk.Label(frame_delete, text="Label:").grid(row=0, column=0, sticky="e")
        self.delete_label_entry = tk.Entry(frame_delete)
        self.delete_label_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Button(frame_delete, text="Delete", command=self.delete_credential).grid(row=1, column=0, columnspan=2, pady=10)

        # Bottom frame with save and exit button
        frame_bottom = tk.Frame(self.vault_management_frame)
        frame_bottom.pack(padx=10, pady=10, fill="x")
        tk.Button(frame_bottom, text="Save and Exit", command=self.create_start_frame).pack(ipadx=5, ipady=5)

    # Creates a new vault file
    def create_vault(self):

        # Get user input for vault name and password
        vault_name = self.create_vault_name_entry.get()
        master_password = self.create_master_password_entry.get()

        # Create new vault file
        try:
            self.manager.create_credential_file(vault_name + ".vault", master_password)
            self.create_vault_management_frame()
        except Exception as e:
            print(f"Error: {str(e)}")

    # Opens an existing vault file
    def open_vault(self):

        # Get user input for vault name and password
        vault_name = self.open_vault_name_entry.get()
        master_password = self.open_master_password_entry.get()

        # Open vault file
        try:
            self.manager.load_credential_file(vault_name + ".vault", master_password)
            self.create_vault_management_frame()
        except Exception as e:
            print(f"Error: {str(e)}")

    def add_credential(self):
        pass

        # TODO: Add credentials to vault file from entry fields

    def load_edit_fields(self):
        self.edit_fields_frame.grid()

        # TODO: Load credentials into entry fields for editing

    def edit_credential(self):
        self.edit_fields_frame.grid_remove()

        # TODO: Edit credentials in vault with new values in edit entry fields

    def delete_credential(self):
        pass

        # TODO: Delete all credentials of given label

if __name__ == "__main__":
    cmgui = CredentialManagerGUI()
    cmgui.root.mainloop()