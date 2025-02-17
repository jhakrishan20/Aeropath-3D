import tkinter as tk
from tkinter import messagebox
import requests  
import time
import threading
import json
# from app_gui import check_connection 

class MenuBar:

    def __init__(self, root):
        self.root = root
        self.menubar = tk.Menu(self.root)
        self.create_menus()

    def create_menus(self):
        # Mission Menu
        mission_menu = tk.Menu(self.menubar, tearoff=0)
        mission_menu.add_command(label="New Mission", command=self.new_mission)
        mission_menu.add_command(label="Load Mission", command=self.load_mission)
        mission_menu.add_command(label="Save Mission", command=self.save_mission)
        mission_menu.add_separator()
        # mission_menu.add_command(label="Exit", command=self.exit_app)


        # Edit Menu
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        # edit_menu.add_command(label="Undo", command=self.undo)
        # edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        # edit_menu.add_command(label="Preferences", command=self.preferences)

        # Help Menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Check Connection", command=self.check_connection)
        help_menu.add_command(label="Troubleshoot", command=self.restart_server)
        help_menu.add_command(label="Diagnostics", command=self.diagnostics)

        # Add menus to menubar
        self.menubar.add_cascade(label="Mission", menu=mission_menu)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        self.menubar.add_cascade(label="Help", menu=help_menu)

        # Attach the menubar to the root window
        self.root.config(menu=self.menubar)


        #.
        #.
        # Command Functions
    def new_mission(self):
        messagebox.showinfo("Mission", "Create a new mission.")

    def load_mission(self):
        messagebox.showinfo("Mission", "Load an existing mission.")

    def save_mission(self):
        messagebox.showinfo("Mission", "Save the current mission.")

    def check_connection(self):
        messagebox.showinfo("Help", "checking" )

    def restart_server(self):
        messagebox.showinfo("Help", "Restarting server...")
         # Define the endpoint URL for restarting the server
        url = "http://127.0.0.1:5001/restart" 

        try:
            # Send a POST request (or GET, depending on your endpoint)
            response = requests.post(url)  # Change to requests.get() if it's a GET request

            if response.status_code == 200:
                print("Server restarted successfully!")
                tk.messagebox.showinfo("Success", "Server restarted successfully!")
            else:
                print("Failed to restart the server.")
                tk.messagebox.showerror("Error", "Failed to restart the server.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            tk.messagebox.showinfo("Success", "Closed existing connection and restarted!")
            # tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def diagnostics(self):
        messagebox.showinfo("Help", "under development....")    