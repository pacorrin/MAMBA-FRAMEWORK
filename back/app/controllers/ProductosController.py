from core.AppController import AppController
from app.models.Productos import Productos
from flask_classy import route

class ProductosControllerView(AppController):

    def __init__(self):
        super().__init__()
        self.Productos = Productos()
        
    @route('/', methods=['GET'])
    def consultar(self):
        return self.Productos.consultar()
    
    @route('/<id>', methods=['GET'])
    def consultarUno(self, id):
        return self.Productos.consultarUno(id)

    @route('/guardar', methods=['POST'])
    def guardar(self):
        return self.Productos.guardar(self.request)

    @route('/actualizar', methods=['PUT'])
    def actualizar(self):
        return self.Productos.actualizar()

    @route('/eliminar/<id>', methods=['DELETE'])
    def eliminar(self, id):
        return self.Productos.eliminar(id)        
