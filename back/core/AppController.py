from flask_classy import FlaskView
from flask import request

class AppController(FlaskView):
    request = None

    def __init__(self):
        self.request = request
        pass

