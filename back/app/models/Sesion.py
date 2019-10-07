
from core.AppModel import AppModel
import hashlib as hl
from datetime import datetime
import json

class Sesion(AppModel):

    def __init__(self):
        super().__init__()

    def login(self, request):
        data = request.get_json()
        mail = data["mail"].encode('utf-8').__str__()
        print(mail)
        res = self.dbDriver.query('SELECT * from usuarios', {
            "mail =" : data["mail"],
            "pass =" : str(hl.sha512(data["password"].encode('utf-8')).hexdigest()),
        }, resType="array")
        if len(res) > 0:
            dt = datetime.now().timestamp().__str__()
            strToHash = dt + mail.encode('utf-8').__str__()
            token = hl.sha512(strToHash.encode('utf-8')).hexdigest()
            res = self.dbDriver.query('INSERT INTO sesiones', [
                            "NULL",
                            token,
                            res[0][0],
                            "NOW()",
                            1
                        ])
            if res:
                return json.dumps({"token": token,"exito": True})
            else:
                return json.dumps({ "msg" : "No se pudo registrar la sesión", "exito": False})
        else:
            return str(json.dumps({ "msg" : "Error al inicia sesión", "exito": False}))

    
    def validar(self, request):
        data = request.get_json()
        sesion = self.dbDriver.query('SELECT * from sesiones', {
            "token =" : data["token"],
            "status =" : "1"
        }, resType="array")
        if len(sesion) > 0:
            return json.dumps({"valido": True})
        else:
            return json.dumps({"valido": False})
  

    def cerrar(self, request):
        return self.dbDriver.query('INSERT' ,{
            "field1" : "value",
            "field2" : "value",
            "field3" : "value",
        })
