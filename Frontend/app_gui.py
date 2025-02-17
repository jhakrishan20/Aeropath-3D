# app_gui.py
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox, ttk, Frame, Label
from PIL import Image, ImageTk
from login_gui import LoginFrame  # Import LoginFrame class from login_frame.py
from menubar_gui import MenuBar
import requests  
import time
import threading
import json

#global var to check drone connection
check_connection = "not connected"

class SIDAKApp:

    def __init__(self, root):
        self.root = root
        self.root.title("SIDAK Path Planner v1.0.0")
        self.root.geometry("920x620")  # Set window to fit the main frame

        # Initialize LoginFrame with a callback to show the main UI on successful login
        self.login_frame = LoginFrame(root, self.show_main_ui)

        # Create the main frame with specified dimensions but keep it hidden initially
        self.main_frame = tk.Frame(root, width=920, height=620)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack_forget()  

    def show_main_ui(self):

        # integrate menubar
        self.menu_frame = MenuBar(root)

        # create main ui
        self.create_main_ui()
        self.main_frame.pack(fill="both", expand=True)    

    def create_main_ui(self):

        # TCP Port Input Section
        port_frame = tk.Frame(self.main_frame)
        port_frame.pack(pady=10)

        tk.Label(port_frame, text="TCP Port:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.port_entry = tk.Entry(port_frame, width=15, font=("Arial", 12))
        self.port_entry.pack(side=tk.LEFT, padx=10)
        self.port_value = self.port_entry.get()

        # Connection status label next to the TCP port input box
        self.connection_status_label = tk.Label(port_frame, text="Not Connected", fg="red", font=("Arial", 10))
        self.connection_status_label.pack(side=tk.LEFT, padx=10)

        # Connect to mav mirror stream
        connect_frame = tk.Frame(self.main_frame)
        connect_frame.pack(pady=10)
        self.connect_button = tk.Button(connect_frame, text="Connect to MAV mirror", command=self.connect_to_drone, font=("Arial", 12))
        self.connect_button.pack()

        # # Mission Type Section
        # mission_type_frame = tk.LabelFrame(self.main_frame, text="Mission Type", padx=10, pady=10, font=("Arial", 12))
        # mission_type_frame.pack(padx=20, pady=10, fill="both")

        # # Dropdown menu for Mission Type
        # self.mission_type = tk.StringVar(value="Normal Mission")
        # mission_types = ["Normal Mission", "Obstacle Mission"]

        # tk.OptionMenu(mission_type_frame, self.mission_type, *mission_types).pack(side="left", padx=10)

        # Mission Type and Camera Angle Section (placed horizontally side by side)
        mission_camera_frame = tk.Frame(self.main_frame)
        mission_camera_frame.pack(padx=20, pady=10, fill="both")

        # Mission Type Dropdown Menu
        self.mission_type = tk.StringVar(value="Normal Mission")
        mission_types = ["Normal Mission", "Obstacle Mission"]
        tk.Label(mission_camera_frame, text="Mission Type:", font=("Arial", 12)).pack(side="left", padx=10)
        tk.OptionMenu(mission_camera_frame, self.mission_type, *mission_types).pack(side="left", padx=10)

        # Camera Angle Dropdown Menu
        self.cam_option = tk.StringVar()
        self.cam_option.set("Manual")
        cam_options = ["Manual", "Present", "Look at Tower", "Look Full Tower"]
        tk.Label(mission_camera_frame, text="Camera Angle:", font=("Arial", 12)).pack(side="left", padx=10)
        tk.OptionMenu(mission_camera_frame, self.cam_option, *cam_options).pack(side="left", padx=10)   

        # mission control Dropdown Menu
        self.control_option = tk.StringVar()
        self.control_option.set("Manual")
        control_options = ["Manual", "Auto"]
        tk.Label(mission_camera_frame, text="Control Options:", font=("Arial", 12)).pack(side="left", padx=10)
        tk.OptionMenu(mission_camera_frame, self.control_option, *control_options).pack(side="left", padx=10)       

        # Mission Parameters Section
        mission_frame = tk.LabelFrame(self.main_frame, text="Mission Parameters", padx=10, pady=10, font=("Arial", 12))
        mission_frame.pack(padx=20, pady=20, fill="both")

        tk.Label(mission_frame, text="Starting Latitude:", font=("Arial", 10)).grid(row=0, column=0, sticky="e")
        self.start_lat_entry = tk.Entry(mission_frame, font=("Arial", 10))
        self.start_lat_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(mission_frame, text="Starting Longitude:", font=("Arial", 10)).grid(row=0, column=2, sticky="e")
        self.start_long_entry = tk.Entry(mission_frame, font=("Arial", 10))
        self.start_long_entry.grid(row=0, column=3, padx=5, pady=5)

        # Center Latitude and Longitude added
        tk.Label(mission_frame, text="Center Latitude:", font=("Arial", 10)).grid(row=1, column=0, sticky="e")
        self.center_lat_entry = tk.Entry(mission_frame, font=("Arial", 10))
        self.center_lat_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(mission_frame, text="Center Longitude:", font=("Arial", 10)).grid(row=1, column=2, sticky="e")
        self.center_long_entry = tk.Entry(mission_frame, font=("Arial", 10))
        self.center_long_entry.grid(row=1, column=3, padx=5, pady=5)

        # Geo Avg Start Button
        self.geo_avg_button = tk.Button(mission_frame, text="Geo Avg Start", font=("Arial", 10), command=self.calculate_geo_avg)
        self.geo_avg_button.grid(row=1, column=4, padx=10, pady=5)
        
        # tower parameters section
        tower_frame = tk.LabelFrame(self.main_frame, text="Tower Parameters", padx=10, pady=10, font=("Arial", 12))
        tower_frame.pack(padx=20, pady=10, fill="both")

        tk.Label(tower_frame, text="Tower Height(m):", font=("Arial", 10)).grid(row=0, column=0, sticky="e")
        self.height_entry = tk.Spinbox(tower_frame, font=("Arial", 10))
        self.height_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(tower_frame, text="Tower Radius(m):", font=("Arial", 10)).grid(row=0, column=2, sticky="e")
        self.radius_entry = tk.Spinbox(tower_frame, font=("Arial", 10))
        self.radius_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(tower_frame, text="Starting Alt(m):", font=("Arial", 10)).grid(row=0, column=4, sticky="e")
        self.start_alt_entry = tk.Spinbox(tower_frame, font=("Arial", 10))
        self.start_alt_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(tower_frame, text="Vertical Descent(m):", font=("Arial", 10)).grid(row=1, column=0, sticky="e")
        self.vdescent_entry = tk.Spinbox(tower_frame, font=("Arial", 10))
        self.vdescent_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(tower_frame, text="Stopping Alt(m):", font=("Arial", 10)).grid(row=1, column=2, sticky="e")
        self.spiral_count_entry = tk.Spinbox(tower_frame, font=("Arial", 10))
        self.spiral_count_entry.grid(row=1, column=3, padx=5, pady=5)

        # tk.Label(tower_frame, text="Angle Increment(°):", font=("Arial", 10)).grid(row=1, column=4, sticky="e")
        # self.ang_inc_entry = tk.Spinbox(tower_frame, font=("Arial", 10))
        # self.ang_inc_entry.grid(row=1, column=5, padx=5, pady=5)

        tk.Label(tower_frame, text="dist_bw_wp(m):", font=("Arial", 10)).grid(row=1, column=4, sticky="e")
        self.dist_bw_wp = tk.Spinbox(tower_frame, font=("Arial", 10))
        self.dist_bw_wp.grid(row=1, column=5, padx=5, pady=5)


        # Camera Parameters Section
        camera_frame = tk.LabelFrame(self.main_frame, text="Camera Parameters", padx=10, pady=10, font=("Arial", 12))
        camera_frame.pack(padx=20, pady=10, fill="both")

        tk.Label(camera_frame, text="Focal Length (mm):", font=("Arial", 10)).grid(row=0, column=0, sticky="e")
        self.focal_length_entry = tk.Entry(camera_frame, font=("Arial", 10))
        self.focal_length_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(camera_frame, text="Image Width (px):", font=("Arial", 10)).grid(row=0, column=2, sticky="e")
        self.image_width_entry = tk.Entry(camera_frame, font=("Arial", 10))
        self.image_width_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(camera_frame, text="Image Height (px):", font=("Arial", 10)).grid(row=0, column=4, sticky="e")
        self.image_height_entry = tk.Entry(camera_frame, font=("Arial", 10))
        self.image_height_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(camera_frame, text="Sensor Width (mm):", font=("Arial", 10)).grid(row=1, column=0, sticky="e")
        self.sensor_width_entry = tk.Entry(camera_frame, font=("Arial", 10))
        self.sensor_width_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(camera_frame, text="Sensor Height (mm):", font=("Arial", 10)).grid(row=1, column=2, sticky="e")
        self.sensor_height_entry = tk.Entry(camera_frame, font=("Arial", 10))
        self.sensor_height_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(camera_frame, text="Overlap (%):", font=("Arial", 10)).grid(row=1, column=4, sticky="e")
        self.overlap_entry = tk.Entry(camera_frame, font=("Arial", 10))
        self.overlap_entry.grid(row=1, column=5, padx=5, pady=5)

        # Submit Button to generate way points
        submit_button = tk.Button(self.main_frame, text="Generate Way Points", font=("Arial", 12), command=self.generate_wps)
        submit_button.pack(pady=10)


    # .
    # .
    # .
    def connect_to_drone(self):
        global check_connection
        port_no = self.port_entry.get()
        if port_no =='14550':
         try:
            # Send a POST request to the Flask server to initiate drone connection and recieve response
            response = requests.post("http://127.0.0.1:5001/connect", json={"port_no": port_no})
            response_data = response.json()
            message = response_data.get("message") #parse the json message

            if response.status_code == 200:
                self.connection_status_label.config(text="Connected", fg="green")
                messagebox.showinfo("Connection", message)
                check_connection = "0"

                # Listen to the SSE endpoint in a new thread to avoid blocking the UI
                status_thread = threading.Thread(target=self.receive_status_updates, daemon=True)
                status_thread.start()
                
            else:
                self.connection_status_label.config(text="Not Connected", fg="red")
                messagebox.showerror("Connection", message)
                check_connection = "1"
         
         except requests.exceptions.RequestException as e:
            # Show error message if there is an issue with the server connection
            print(f"Error: {str(e)}")
            messagebox.showerror("Connection", "server not running")
        else:messagebox.showerror("Connection", "! Invalid Port Number !")

    #recieve status updates        
    def receive_status_updates(self):
        print("monitoring connection")
        try:
            # Connect to the connection status stream
            with requests.get("http://127.0.0.1:5001/connection-status", stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        # Parse JSON status update
                        status_update = json.loads(line.decode('utf-8').replace("data: ", ""))
                        status = status_update.get("status")
                        print(status)

                        # Update the UI based on the current status
                        if status == "Connected":
                            self.connection_status_label.config(text="Connected", fg="green")
                            return 0
                        elif status == "Disconnected":
                            self.connection_status_label.config(text="Disconnected", fg="red")
                            messagebox.showerror("Connection", "Drone connection lost.")
                            return 1
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("Connection", "Unable to connect to status stream")
    
    # function triggered when geo avg start button is clicked
    def calculate_geo_avg(self):

        if check_connection == "0":
           
           # Create a top-level window as a loader
           self.loader_window = tk.Toplevel(self.root)
           self.loader_window.title("Calculating...")
           self.loader_window.geometry("300x100")
           self.loader_window.transient(self.root)  # Keep the loader window on top of the main window
           self.loader_window.grab_set()  # Block interaction with the main window
           tk.Label(self.loader_window, text="Calculating Geographic Average...", font=("Arial", 10)).pack(pady=10)

         # Add a Progressbar widget in indeterminate mode
           progress = ttk.Progressbar(self.loader_window, mode="indeterminate", length=200)
           progress.pack(pady=10)
           progress.start()  # Start the progress animation 

           # Run the loader window thread seperately  to avoid freezing the UI 
           calculation_thread = threading.Thread(target=self.geo_avg_loader_window, args=(progress,))
           calculation_thread.daemon = True  # Optional: allows thread to exit when the main program exits
           calculation_thread.start()

           #Run the telemtry thread to hit the /start_telemetry endpoint
           telemetry_thread = threading.Thread(target=self.start_telemetry, args=())
           telemetry_thread.daemon = True
           telemetry_thread.start()

        else:
            messagebox.showerror("Connection", "Drone not connected") 

    # function just makes a loader window for 20s to demonstarte the ongoing calc.
    def geo_avg_loader_window(self, progress):   
        time.sleep(20)  # Placeholder for actual calculation
        progress.stop()
        self.loader_window.destroy()

        # Show a message box with the result
        messagebox.showinfo("Geo Avg Start", "! Geographic Average Calculation Complete !")

    # function with api to hit the /start_telemetry endpoint
    def start_telemetry(self):
     try:
        response = requests.post('http://127.0.0.1:5001/start_telemetry')
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            print("Telemetry started!")
            time.sleep(20)  # Let it run for 20 seconds
            try:
                self.fetch_telemetry_data()
            except Exception as e:
                print(f"Error in fetch_telemetry_data: {e}")
     except requests.exceptions.RequestException as e:
        print(f"Error connecting to backend: {e}")

    # function to fetch the calculated average from the server
    def fetch_telemetry_data(self):
        print("win1...")
        # Here perform an API call to fetch telemetry data from the server
        response = requests.get("http://127.0.0.1:5001/get_telemetry")
        print(response.text)
        if response.status_code == 200:
            avg_gps = response.json().get("average_gps")
            print(avg_gps)
            average_lat = avg_gps[0]
            average_long = avg_gps[1]
            print(average_lat)
            
            self.display_gps_avg(average_lat, average_long)  # Pass lat and long to display method
            return avg_gps
        else:
            print("Failed to fetch telemetry data")
            return []    
        
    # Function to display GPS average in the entry fields
    def display_gps_avg(self, average_lat, average_long):
        # Set the values in the entry fields
        self.center_lat_entry.delete(0, tk.END)  # Clear any existing value
        self.center_lat_entry.insert(0, f"{average_lat:.6f}")  # Insert latitude with precision
    
        self.center_long_entry.delete(0, tk.END)  # Clear any existing value
        self.center_long_entry.insert(0, f"{average_long:.6f}")  # Insert longitude with precision
    # .
    # .
    # .
    def generate_wps(self):

        tower_lats = self.center_lat_entry.get()   
        tower_longs = self.center_long_entry.get()   
        height = self.height_entry.get()
        radius  = self.radius_entry.get()
        start_altitude = self.start_alt_entry.get()
        vertical_interval = self.vdescent_entry.get()
        stop_altitude = self.spiral_count_entry.get()
        dist_bw_wp = self.dist_bw_wp.get()
        focal_length = self.focal_length_entry.get()
        sensor_width = self.sensor_width_entry.get()
        sensor_height = self.sensor_height_entry.get()
        overlap = self.overlap_entry.get()
    
        if height and radius and start_altitude and vertical_interval and stop_altitude and dist_bw_wp and tower_lats and tower_longs and focal_length and sensor_height and sensor_width and overlap:
         url = "http://127.0.0.1:5001/tower_params"
         data = {
         "tower_lats": tower_lats,
         "tower_longs": tower_longs,
         "height": height,
         "radius": radius,
         "start_alt": start_altitude,
         "vertical_intv": vertical_interval,
         "stop_alt": stop_altitude,
         "dist_bw_wp": dist_bw_wp,
         "focal_length": focal_length,
         "sensor_width": sensor_width,
         "sensor_height": sensor_height,
         "overlap": overlap  }

         if start_altitude == stop_altitude:
            messagebox.showinfo("Way Points", "start and stop altitude couldnt be same")
         #  print(data)
         try:
           # Send JSON data
           res = requests.post(url, json={"data": data})
        
           # Check the response status
           if res.status_code == 201:
               result = res.json().get("message", "No message received")
               tk.Label(self.root, text=f"Result: {result}").pack()
               messagebox.showinfo("Way Points", result)
           elif res.status_code == 500:
            error_message = res.json().get("error", "Internal server error")
            tk.Label(self.root, text=f"Error: {error_message}").pack()
            messagebox.showinfo("Way Points", error_message)
           else:
               tk.Label(self.root, text=f"Error: Unexpected response {res.status_code}").pack()
           # Simulating a potential error
           raise IndexError("Example IndexError")    
         except IndexError as e:
           data = {"error_message": str(e)}  # Serialize the error message as a string
           response = requests.post(url, json=data)
           print(response.status_code, response.json())
        else:
         messagebox.showinfo("Way Points", "! Enter all tower parameters !")

    # .
    # .
    # .




if __name__ == "__main__":
 root = tk.Tk()
 app = SIDAKApp(root)
 app.login_frame.show()  # Show login screen first
 root.mainloop()
 print("closing application")
