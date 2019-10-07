
class permisos_usuario():
    fields = {
        "id": ["INT", "AUTO_INCREMENT"], 
        "idPermiso": ["INT", "NOT NULL"], 
        "idUsuario": ["VARCHAR(45)", "NOT NULL"], 
    }

    def __init__(self):
         pass