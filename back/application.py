from flask import Flask
from flask_cors import CORS
from router import routes
import importlib

base_path_controllers = 'app.controllers.'

class App:
    app = None

    def __init__(self):
        self.app = Flask(__name__)
        # cors = CORS(self.app, resources={r"/*": {"origins": "http://localhost:3000/*"}})
        cors = CORS(self.app)
        self.loadControllers()

    def loadControllers(self):
        for route in routes:
            cls = getattr(importlib.import_module(base_path_controllers + routes[route]['module']), routes[route]['class'])
            cls.register(self.app, route_base=route)
        
    def run(self):
        self.app.run()
        return self