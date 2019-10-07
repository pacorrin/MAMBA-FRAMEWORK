
class sesiones():
    fields = {
        "id": ["INT", "AUTO_INCREMENT"], 
        "token": ["VARCHAR(150)", "NOT NULL"], 
        "idUsuario": [ "INT","NOT NULL" ],
        "fecha":  ["DATETIME", "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"],
        "status":  ["BIT", "NOT NULL DEFAULT 1"]
    }

    def __init__(self):
         pass