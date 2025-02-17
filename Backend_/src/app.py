from flask import Flask
from routes.routes import Api

# Initialize and run the Flask server
if __name__ == '__main__':
    # Run the Flask server
    app = Flask(__name__)
    routes = Api()
    app.register_blueprint(routes.routes)
    app.run(host='0.0.0.0', port=5001, debug=True)
    