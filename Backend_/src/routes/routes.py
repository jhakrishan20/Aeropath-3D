from flask import Blueprint, jsonify, Response, request
from connector.connection import Connection
from connector.telemetry import Telemetry

class Routes:
    def register_routes(self):
        self.routes.add_url_rule('/connect', 'connect', self.start_connection, methods=['POST'])
        self.routes.add_url_rule('/connection-status', 'check_connection', self.check_connection, methods=['GET'])
        self.routes.add_url_rule('/start_telemetry', 'start_telemetry', self.start_telemetry, methods=['POST'])
        self.routes.add_url_rule('/get_telemetry', 'get_telemetry', self.get_telemetry, methods=['GET']) 
        self.routes.add_url_rule('/restart', 'restart', self.restart_server, methods=['POST']) 

class Api(Routes):
    def __init__(self):
        # Initialize the Flask Blueprint
        self.routes = Blueprint("routes", __name__)
        self.connection = None
        self.telemetry = None
        self.conn_res = False
        self.telem_res = None

        # Register all routes
        self.register_routes()

    def start_connection(self):
        try:
            port = "14550"  # Default port for the connection
            self.connection = Connection(port)  # Initialize connection object
            self.conn_res = self.connection.connect()  # Initiate the connection

            if self.conn_res == True:
                return jsonify({"message": "Drone Connected Successfully"}), 200
            else:
                return jsonify({"message": "Failed to Connect to Drone"}), 500
        except Exception as e:
            print(f"Error during connection: {e}")
            return jsonify({"message": "An error occurred during connection"}), 500

    def check_connection(self):
        try:
            if not self.connection:
                return jsonify({"message": "Drone is not connected"}), 400

            self.connection.connection_status_stream()
            return Response(content_type="text/event-stream")
        except Exception as e:
            print(f"Error in connection status stream: {e}")
            return jsonify({"message": "Error in connection status stream"}), 500

    def start_telemetry(self):
        try:
            if self.conn_res == True:
                self.telemetry = Telemetry(self.connection)
                self.telemetry.start_telemetry()
                return jsonify({"message": "Telemetry started!"}), 200
            else:
                return jsonify({"message": "Drone is not connected"}), 400
        except Exception as e:
            print(f"Error starting telemetry: {e}")
            return jsonify({"message": "Error starting telemetry"}), 500

    def get_telemetry(self):
        try:
            self.telem_res = self.telemetry.get_telemetry_data() or [0,0,0]
            print(self.telem_res)
            if self.telem_res:
                return jsonify({"average_gps": self.telem_res}), 200
            else:
                return jsonify({"message": "Telemetry is not available"}), 400
        except Exception as e:
            print(f"Error retrieving telemetry: {e}")
            return jsonify({"message": "Error retrieving telemetry"}), 500
    
    def restart_server(self):
        try:
            if self.connection.restart() == True:
               return "Server restarting...", 200
        except Exception as e:
               return f"Error: {str(e)}", 500   