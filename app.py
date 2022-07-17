import os
from model.empleados import empleados
from model.cargos import cargos
from model.cartaPedidos import cartaPedidos
from util.Aplication import Aplication
from model.categorias_routes import categorias
from model.platillos_routes import platillos
# agregado para foto
from datetime import datetime
from flask import request, jsonify, make_response
from util.Connection import Connection
# from model.pruebas import pruebas

aplication = Aplication()
conexion = Connection()
app = aplication.app
input_images_path2 = '\Repositorios/backEnd/upload/'
input_images_path = '\Repositorios/backEnd/upload/'
mysql = conexion.mysql
CARPETAUP = os.path.join('/Repositorios/backEnd/upload/')
# files_names = os.listdir(CARPETAUP)
# print(files_names)
app.config['CARPETAUP'] = CARPETAUP


app.register_blueprint(empleados)
app.register_blueprint(categorias)
app.register_blueprint(platillos)
app.register_blueprint(cargos)
app.register_blueprint(cartaPedidos)
@app.route("/pedido/update/<int:id>/", methods=["PUT"])
def empleadoCreateUpdate2(id):
    try:
        # nombreProducto = request.form["txtnombreProducto"]
        # precioProducto = request.form["txtprecio"]
        imagenProducto = request.files["txtimagen"]
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        mensaje = ""
        sql = ""
        if imagenProducto.filename != '':
            cambioNombre = tiempo+imagenProducto.filename
            sql = "SELECT foto from misfotos WHERE id = (%s);"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, (id))
            fila = cursor.fetchall()
            valor = str(os.path.join(app.config['CARPETAUP'],fila[0][0]))
            print("el removido es: ", valor)
            os.remove(os.path.join(app.config['CARPETAUP'],fila[0][0]))
            
            sql2 = "UPDATE misfotos SET foto = %s WHERE id=%s;"
            cursor.execute(sql2, (cambioNombre, id))
            conn.commit()
            imagenProducto.save(input_images_path + cambioNombre)
            mensaje ="foto actualizada"
        else: 
            mensaje="no se que paso pero no se actualizo x'd"
    except Exception as ex:
        mensaje = "falla: " + repr(ex)
    return jsonify({"mensaje": mensaje})

def pagina_no_encontrada(error):
    return "<h1>Método no encontrado</h1>"

@app.route("/")
def ingreso():
    return "<h1>corriendo :)</h1>"

# @app.route("/curso/foto/<string:imagen>/", methods = ['GET'])
# def cargarImagen(imagen):
#     image_data = open("upload/"+imagen, "rb").read()
#     resultado = make_response(image_data)
#     resultado.headers['Content-Type'] = 'image/png'
#     return resultado

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
