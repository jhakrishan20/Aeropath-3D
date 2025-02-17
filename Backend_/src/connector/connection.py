import threading, time, json, os, sys
from pymavlink import mavutil

class Connection:
   
    def __init__(self, port_no):
        self.__connection_string = 'tcp:127.0.0.1:'
        self.port_no = port_no
        self.connection_status = {"status": "Not Connected"}
        self.previous_status = None
        self.current_status = None
        self.vehicle = None

    def connect(self):

        # Update the connection string
        connection_string = self.__connection_string + str(self.port_no)
        
        # Start the connection process in a separate thread
        self.connection_status["status"] = "Not Connected"
        connection_thread = threading.Thread(target=self.connect_to_vehicle(connection_string))
        connection_thread.start()

        # Wait for the connection to complete by checking the status
        while self.connection_status["status"] == "Not Connected":
           time.sleep(0.1)  # Short delay to prevent busy waiting
        
        if self.connection_status["status"] == "Connected":
           print("connected.......")
           return True

        else:
            print("not connected")
            return False
    
    def connect_to_vehicle(self, connection_string):
    
        try:
            print("Connecting to vehicle...")
            self.vehicle = mavutil.mavlink_connection(connection_string)
            print("vehicle ------")
            print(self.vehicle)

            # Wait for heartbeat with timeout
            start_time = time.time()
            while time.time() - start_time < 10:
                try:
                 self.vehicle.wait_heartbeat(blocking=False)
                 print("Connection established with vehicle!")
                 self.connection_status["status"] = "Connected"
                 return 
                except Exception as e:
                 time.sleep(1)  # Wait briefly and retry
                 print("Waiting for heartbeat...")

            raise TimeoutError("Heartbeat not received within the timeout period.")
        except Exception as e:
                print(f"Failed to connect: {str(e)}")
                self.connection_status["status"] = "Not connected"    
        return self.vehicle            

    def connection_status_stream(self):

        while True:
            self.current_status = self.connection_status["status"]
            if self.current_status != self.previous_status:
                yield f"data: {json.dumps({'status': self.current_status})}\n\n"
                self.previous_status = self.current_status
            time.sleep(1) 
            # print(self.current_status)
            return self.current_status

    def restart():
     try:
         os.execv(sys.executable, ['python'] + sys.argv)  # Restarts the server
         return True
     except Exception as e:
         return e     