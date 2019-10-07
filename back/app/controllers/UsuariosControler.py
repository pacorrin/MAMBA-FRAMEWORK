
from core.AppController import AppController
from flask_cors import cross_origin
from app.models.Usuario import Usuario
from flask_classy import route

class UsuariosControlerView(AppController):

    
    def __init__(self):
        super().__init__()
        self.Usuario = Usuario()


    @route('/consultar', methods=['GET'])
    @cross_origin()
    def index(self):
        return self.Usuario.consultar()

    @route('/consultar/<id>', methods=['GET'])
    @cross_origin()
    def get(self, id):
        return self.Usuario.consultarUno(id)

    @route('/guardar', methods=['POST'])
    @cross_origin()
    def post(self):
        return self.Usuario.guardar(self.request.get_json())

    @route('/actualizar', methods=['PUT','PATCH'])
    @cross_origin()
    def put(self, data):
        return self.Usuario.actualizar(self.request.get_json())

    @route('/eliminar/<id>', methods=['DELETE'])
    @cross_origin()
    def delete(self, id):
        return self.Usuario.eliminar(id)

    @route('/permisos/<id>', methods=['GET'])
    @cross_origin()
    def getPermisos(self, id):
        return self.Usuario.getPermisos(id)   