from core.AppController import AppController
from flask_cors import cross_origin
from app.models.Sesion import Sesion
from flask_classy import route

class SesionControllerView(AppController):

    def __init__(self):
        super().__init__()
        self.Sesion = Sesion()
                    
    @route('/login', methods=['POST'])
    @cross_origin()
    def login(self):
        return self.Sesion.login(self.request)
                
    @route('/validar', methods=['POST'])
    @cross_origin()
    def validar(self):
        return self.Sesion.validar(self.request)

    @route('/cerrar', methods=['POST'])
    @cross_origin()
    def cerrar(self):
       return self.Sesion.cerrar(self.request)