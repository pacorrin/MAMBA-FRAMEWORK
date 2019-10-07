
# ejemplo routes['route'] = ['module_name', 'class_name']

routes = {}

routes["/productos"] = {
    'module': 'ProductosController', 
    'class': 'ProductosControllerView'
}

routes["/sesion"] = {
    'module': 'SesionController', 
    'class': 'SesionControllerView'
}

routes["/usuarios"] = {
    'module': 'UsuariosControler', 
    'class': 'UsuariosControlerView'
}
