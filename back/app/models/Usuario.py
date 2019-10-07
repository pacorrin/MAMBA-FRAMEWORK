
from core.AppModel import AppModel
import json


class Usuario(AppModel):

    def __init__(self):
        super().__init__()

    def consultar(self):
        return self.dbDriver.query('SELECT id, nombre, apellidoP, apellidoM FROM usuarios', resType="json")

    
    def consultarUno(self, id):
        return self.dbDriver.query('SELECT WHERE <id>')

    def guardar(self, data):
        return self.dbDriver.query('INSERT', data)

    def actualizar(self,data):
        return self.dbDriver.query('UPDATE' , data)

    def eliminar(self, id):
        return self.dbDriver.query('DELETE')

    def getPermisos(self,id):
        res = self.dbDriver.query("""
                    SELECT pu.id, p.descripcion 
                    FROM permisos_usuario pu 
                    INNER JOIN permisos p ON p.id = pu.idPermiso"""
                , {
                    "idUsuario =":  id
                }, resType="json")
        return res
