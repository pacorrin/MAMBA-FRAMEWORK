import configparser
from pathlib import Path

from flask_classy import FlaskView
from database.driver import DBDriver


class AppModel:
    dbDriver = None

    def __init__(self):
        self.initDriver()

    def initDriver(self):
        config = configparser.ConfigParser()
        config.read(str(Path().parent.parent.absolute())  + '/conf.ini')
        self.dbDriver = DBDriver(config)
