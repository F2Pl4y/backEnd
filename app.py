from model.empleados import empleados
from model.cargos import cargos
from util.Aplication import Aplication
from model.categorias_routes import categorias
from model.platillos_routes import platillos
# from model.pruebas import pruebas

aplication = Aplication()
app = aplication.app
app.register_blueprint(empleados)
app.register_blueprint(categorias)
app.register_blueprint(platillos)
app.register_blueprint(cargos)
# app.register_blueprint(pruebas)



def pagina_no_encontrada(error):
    return "<h1>Método no encontrado</h1>"

@app.route("/")
def ingreso():
    return "<h1>corriendo :)</h1>"


if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
