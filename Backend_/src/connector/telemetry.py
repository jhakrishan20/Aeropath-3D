import threading, time
from connector.connection import Connection

class Telemetry:

    def __init__(self,connection):
       self.gps_avg_array=[]
       self.telemetry_data = {"gps": None,"position": None,"attitude": None,"battery": None}
       self.latitude_summation = 0
       self.longitude_summation = 0
       self.altitude_summation = 0
       self.count = 0
       self.vehicle = connection.vehicle

    def start_telemetry(self):
        telemetry_thread = threading.Thread(target=self.update_telemetry_data)
        telemetry_thread.daemon = True
        telemetry_thread.start()  # Start the telemetry thread when this endpoint is hit , returning the gps_avg
        print("win .....")
        # return self.gps_avg_array

    def GPS_avg(self, Lat, Long, Alt):
        self.latitude_summation += Lat
        self.longitude_summation += Long
        self.altitude_summation += Alt
        self.count += 1
        return [self.latitude_summation / self.count, self.longitude_summation / self.count, self.altitude_summation / self.count]     
 
    def update_telemetry_data(self):

        print("inside telem - ",self.vehicle)
        # global position_avg_arr
        start_time = time.time()  # Record the start time
        # print(start_time)
        while True:
            if self.vehicle is None:
                time.sleep(1)
                continue

            msg = self.vehicle.recv_match(blocking=True)
            print(msg)
        
            if msg:
                if msg.get_type() == "GPS_RAW_INT":
                    self.telemetry_data["gps"] = {
                        "latitude": msg.lat / 1e7,
                        "longitude": msg.lon / 1e7,
                        "altitude": msg.alt / 1000
                    }
                
                    gps_avg_array = self.GPS_avg(self.telemetry_data['gps']['latitude'], self.telemetry_data['gps']['longitude'], self.telemetry_data['gps']    ['altitude'])
            
                elif msg.get_type() == "GLOBAL_POSITION_INT":
                    self.telemetry_data["position"] = {
                        "latitude": msg.lat / 1e7,
                        "longitude": msg.lon / 1e7,
                        "altitude": msg.relative_alt / 1000
                        # position_avg_arr = GPS_avg(telemetry_data['gps']['latitude'], telemetry_data['gps']['longitude'], telemetry_data['gps']    ['altitude'])
                    }
            
                # elif msg.get_type() == "ATTITUDE":
                #     telemetry_data["attitude"] = {
                #         "roll": msg.roll,
                #         "pitch": msg.pitch,
                #         "yaw": msg.yaw
                #     }
            
                # elif msg.get_type() == "BATTERY_STATUS":
                #     voltage = msg.voltages[0] / 1000  # mV to V
                #     current = msg.current_battery / 100  # cA to A
                #     telemetry_data["battery"] = {
                #         "voltage": voltage,
                #         "current": current,
                #         "remaining": msg.battery_remaining
                #     }
        
                if time.time() - start_time < 20:
                 print("Telemetry Data-------")
                 print(self.telemetry_data['gps'])
                 print(self.telemetry_data['position'])

                else:
                 break  # Stop the loop after 20 seconds
        
            time.sleep(1)  # Delay to reduce data processing load
        print("the avg of gps values in an array")    
        print(gps_avg_array)
        return gps_avg_array
    
    def get_telemetry_data(self):
       return self.gps_avg_array