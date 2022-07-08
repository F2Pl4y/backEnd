from model.curso_routes import curso
from model.empleados import empleados
from util.Aplication import Aplication

aplication = Aplication()
app = aplication.app
app.register_blueprint(curso)
app.register_blueprint(empleados)


def pagina_no_encontrada(error):
    return "<h1>Método no encontrado</h1>"


if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
