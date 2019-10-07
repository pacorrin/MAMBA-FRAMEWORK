import sys, getopt
from core.Dbuilder import DBuilder

controllerTemplate = """

from core.AppController import AppController
from flask_cors import cross_origin
from flask_classy import route

class #CONTROLLERNAME#View(AppController):

    
    def __init__(self):
        super().__init__()

    @route('/consultar', methods=['GET'])
    @cross_origin()
    def index(self):
        pass

    @route('/consultar/<id>', methods=['GET'])
    @cross_origin()
    def get(self, id):
        pass

    @route('/guardar', methods=['POST'])
    @cross_origin()
    def post(self):
        pass

    @route('/actualizar', methods=['PUT','PATCH'])
    @cross_origin()
    def put(self, data):
        pass

    @route('/eliminar/<id>', methods=['DELETE'])
    @cross_origin()
    def delete(self, id):
        pass
      
"""

controllerTemplateWithModel = """

from core.AppController import AppController
from flask_cors import cross_origin
from app.models.#MODELNAME# import #MODELNAME#
from flask_classy import route

class #CONTROLLERNAME#(AppController):
    
    def __init__(self):
        super().__init__()
        self.#MODELNAME# = #MODELNAME#()

    @route('/consultar', methods=['GET'])
    @cross_origin()
    def index(self):
        return self.#MODELNAME#.consultar()

    @route('/consultar/<id>', methods=['GET'])
    @cross_origin()
    def get(self, id):
        return self.#MODELNAME#.consultarUno(id)

    @route('/guardar', methods=['POST'])
    @cross_origin()
    def post(self):
        return self.#MODELNAME#.guardar(self.request.get_json())

    @route('/actualizar', methods=['PUT','PATCH'])
    @cross_origin()
    def put(self, data):
        return self.#MODELNAME#.actualizar(self.request.get_json())

    @route('/eliminar/<id>', methods=['DELETE'])
    @cross_origin()
    def delete(self, id):
        return self.#MODELNAME#.eliminar(id)
     
"""


modelTemplate = """
from core.AppModel import AppModel
import json

class #MODELNAME#(AppModel):

    def __init__(self):
        super().__init__()

    def consultar(self):
        res = self.dbDriver.query('SELECT')
        return res
    
    def consultarUno(self, id):
        return self.dbDriver.query('SELECT WHERE <id>')

    def guardar(self, data):
        return self.dbDriver.query('INSERT', data)

    def actualizar(self,data):
        return self.dbDriver.query('UPDATE' , data)

    def eliminar(self, id):
        return self.dbDriver.query('DELETE')
"""

viewTemplate = ""

routeTemplate = """

routes["/#ROUTENAME#"] = {
    'module': '#CONTROLLERNAME#', 
    'class': '#CONTROLLERNAME#View'
}
"""

def saveFile(path, content):
    with open(path, 'w') as f: 
        f.write(content)
        f.close()
    
def createController(controllerName, controllerTemplate, modelName = ""):
    controller = ""
    if modelName == "":
        controller = controllerTemplate[0].replace("#CONTROLLERNAME#", controllerName)
    else:
        controller = controllerTemplate[1].replace("#CONTROLLERNAME#", controllerName).replace("#MODELNAME#", modelName)

    saveFile('./app/controllers/' + controllerName + '.py', controller)


def createModel(modelName,  modelTemplate):
    model = modelTemplate.replace("#MODELNAME#", modelName)
    saveFile('./app/models/' + modelName + '.py', model)
    

def addRoute( routeName ,controllerName, routeTemplate ):
    with open("router.py", 'a+') as f:
        route = routeTemplate.replace("#ROUTENAME#", routeName).replace("#CONTROLLERNAME#", controllerName)
        f.write(route)
        f.close()

def createView(viewName, viewTemplate):
    viewTemplate.replace("", "")

def createCrud(modelName, controllerName, routeName, modelTemplate, controllerTemplate, routeTemplate):
    createController(controllerName,["",controllerTemplateWithModel], modelName)
    createModel(modelName, modelTemplate)
    addRoute(routeName, controllerName, routeTemplate)

def renombrarArgumentos(argv):                                          
    arg_names = ['accion', 'recurso', 'nombreRecurso', 'extra', 'extra2']
    return dict(zip(arg_names, argv))

def runBuilder():
    dBuilder = DBuilder()

def main(argv):
    args = renombrarArgumentos(argv)
    if args["accion"] == "--create":
        if args["recurso"] == "controller":
            createController(args["nombreRecurso"], [controllerTemplate ,controllerTemplateWithModel],  args["extra"] if len(args) > 3 else "" )

        elif args["recurso"] == "model":
            createModel(args["nombreRecurso"], modelTemplate)

        elif args["recurso"] == "view":
            pass

        elif args["recurso"] == "route":
            pass

        elif args["recurso"] == "crud":
            createCrud(args["extra2"], args["extra"], args["nombreRecurso"], modelTemplate, controllerTemplate, routeTemplate)
            
    elif args["accion"] == "--dbBuild":
         if args["recurso"] == "run":
             runBuilder()


if __name__ == "__main__":
   main(sys.argv[1:])


# comando de prueba python3.7 creator.py [accion] [recurso] [nombreRecurso] [opcional]

# comando de prueba python3.7 creator.py --create crud /route controller modelo
# comando de prueba python3.7 creator.py --create controller controller modelo
# comando de prueba python3.7 creator.py --create model modelo
# comando de prueba python3.7 creator.py --dbBuild run

# acciones disponibles
#   - create

# recursos disponibles
#   - controller
#   - model
#   - view
#   - crud

# accion = lo que se pretende realizar
# recurso = sobre que se va a realizar la accion
# nombre = el nombre del recurso
# opcional = argumentos extra de los recursos

