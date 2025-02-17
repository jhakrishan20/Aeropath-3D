# login_gui.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginFrame:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success  # Callback for successful login

        # Create the login frame with specified dimensions
        self.login_frame = tk.Frame(root, width=400, height=300)
        self.login_frame.pack_propagate(False)  # Prevent resizing based on content
        self.login_frame.pack(pady=100)

        # Load the image with Pillow
        image = Image.open('C:\\Users\\krishan\\Documents\\sidak\\sidak_softwares\\3D-path generation software\\Frontend\\sidak3.png')
        image = image.resize((250, 80), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        # Display the image
        image_label = tk.Label(self.login_frame, image=self.photo)
        image_label.grid(row=0, columnspan=2, pady=10)

        # Login widgets
        tk.Label(self.login_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.login_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=2, column=1, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 12), command=self.check_login)
        self.login_button.grid(row=3, columnspan=2, pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            self.login_frame.pack_forget()  # Hide login frame
            self.on_login_success()  # Trigger success callback
        else:
            messagebox.showerror("Login Error", "Incorrect username or password.")

    def clear_entries(self):
        """Clears the username and password fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def show(self):
        """Show the login frame."""
        self.login_frame.pack(pady=100)

    def hide(self):
        """Hide the login frame."""
        self.login_frame.pack_forget()
