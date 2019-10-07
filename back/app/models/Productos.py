from core.AppModel import AppModel

class Productos(AppModel):

    nombre = ''
    precio = 0

    def consultar(self):
        return self.dbDriver.query("INSERT INTO usuario VALUES('','prueba2','a.prueba2','d.prueba2')")
    5
    def consultarUno(self, id):
        return self.Productos.consultarUno(id)

    def guardar(self):
        return self.Productos.guardar(self.request)

    def actualizar(self):
        return self.Productos.actualizar()

    def eliminar(self, id):
        return self.Productos.eliminar(id)