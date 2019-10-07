from application import App
from sys import path
from os import getcwd

path.append(getcwd() + "/") 

app = App().run()