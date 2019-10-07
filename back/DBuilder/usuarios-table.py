
class usuarios():
    fields = {
        "id": ["INT", "AUTO_INCREMENT"], 
        "mail": ["VARCHAR(50)", "NOT NULL"], 
        "pass": [ "VARCHAR(150)","NOT NULL" ],
        "nombre": [ "VARCHAR(45)","NOT NULL" ],
        "apellidoP": [ "VARCHAR(45)","NOT NULL" ],
        "apellidoM": [ "VARCHAR(45)","NOT NULL" ],
        "domicilio": [ "VARCHAR(80)","NOT NULL" ],        
        "fechaReg":  ["DATETIME", "NOT NULL DEFAULT CURRENT_TIMESTAMP"]
    }

    def __init__(self):
         pass