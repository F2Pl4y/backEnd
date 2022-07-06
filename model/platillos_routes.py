import re
from flask import Blueprint, jsonify, request, make_response
from util.Connection import Connection
conexion = Connection()
platillos = Blueprint("platillos", __name__)
mysql = conexion.mysql

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)

def platilloGetInterno(id):
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, imagen, descripcion, idCategoria FROM producto WHERE estado = 1 AND idProducto = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idProducto": dato[0],
                "nombreProducto": dato[1],
                "precio": dato[2],
                "imagen": dato[3],
                "descripcion": dato[4],
                "idCategoria": dato[5]
            }
        else:
            resultado = "No se ha encontrado el producto"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error: "+repr(ex)
        exito = False
    return [resultado, exito]

@platillos.route("/platillos/select/", methods=["GET"])
def platillsoSelect():
    resultado = []
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, descripcion, idCategoria FROM producto WHERE estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                DatosProducto = {
                    "idProducto": fila[0],
                    "nombreProducto": fila[1],
                    "precio": fila[2],
                    "descripcion": fila[3],
                    "idCategoria": fila[4]
                }
                resultado.append(DatosProducto)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@platillos.route("/platillos/get/<int:id>", methods=["GET"])
def platilloGet(id):
    dato = platilloGetInterno(id)
    return jsonify({"resultado": dato[0], "exito": dato[1]})


@platillos.route("/platillos/foto/<int:id>/", methods = ['GET'])
def cargarImagenPlatillo(id):
    dato = platilloGetInterno(id)
    if dato[1] == True:
        image_data = open("upload/images/"+dato[0]["imagen"], "rb").read()
        resultado = make_response(image_data)
        resultado.headers['Content-Type'] = 'image/png'
    else:
        resultado = jsonify({"resultado": dato[0], "exito": dato[1]})
    return resultado

@platillos.route("/platillos/delete/<int:id>/", methods = ['PUT'])
def platillosDelete(id):
    try:
        sql = "UPDATE producto SET estado = 0 WHERE idProducto=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        conector.commit()
        mensaje = ""
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error "+repr(ex)
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})


def platillosGetCategoria(id):
    exito = True
    try:
        sql = "SELECT idCategoria, nombreCategoria FROM categoria WHERE idCategoria=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idCategoria": dato[0],
                "nombreCategoria": dato[1]
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error: "+repr(ex)
        exito = False
    return [resultado, exito]

@platillos.route("/platillos/create/", methods=["POST"])
def platilloInsert():
    try:
        print("hola")
        nombrePlatillo = request.form["txtNombrePlatillo"]
        precio = request.form["txtPrecio"]
        imagen = request.files['imagenPlatillo']
        descripcion = request.form["txtDescripcion"]
        idCategoria = request.form["txtIdCategoria"]
        print("hola")

        nombrePlatillo = strip_tags(nombrePlatillo)
        precio = strip_tags(precio)
        descripcion = strip_tags(descripcion)
        idCategoria = strip_tags(idCategoria)
        print("hola")

        if imagen != None:
            print(idCategoria)
            nombreCategoria = platillosGetCategoria(idCategoria)[0]["nombreCategoria"]
            print("hola")
            nombreCategoria = "".join(nombreCategoria.split())
            print("hola")
            ruta = nombreCategoria+"/"+imagen.filename
            print("hola")
            imagen.save("upload/images/"+ruta)
            print("hola")
            sql = "INSERT INTO producto(nombreProducto, precio, imagen, descripcion, idCategoria) VALUES (%s, %s, %s, %s, %s)"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, [nombrePlatillo, precio, ruta, descripcion, idCategoria])
            conn.commit()
            print("hola")
            mensaje = ""
        else:
            mensaje = "Es necesario que insertes una imagen"
    except Exception as ex:
        mensaje = "Error en la ejecucion "+repr(ex)
    return jsonify({"mensaje": mensaje})