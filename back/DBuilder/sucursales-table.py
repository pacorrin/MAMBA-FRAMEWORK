class sucursales():
    fields = {
        "id": ["INT", "AUTO_INCREMENT"], 
        "nombre": ["VARCHAR(45)", "NOT NULL"], 
        "domicilio": [ "VARCHAR(45)","NOT NULL" ],
        "descripcion": [ "VARCHAR(100)","NOT NULL" ],
    }

    def __init__(self):
         pass