# drivers
from database.dbdrivers.mysql import mysql
from database.dbdrivers.sqlite import sqlite


class DBDriver:  
    def __new__(cls, conf):
        return globals()[conf['DATABASE']['DRIVER']](conf)