import os
import re
from flask import Blueprint, jsonify, request, make_response
from util.Connection import Connection
from datetime import datetime
import json

# para las fotos
# from util.Aplication import Aplication


conexion = Connection()
cartaPedidos = Blueprint("cartaPedidos", __name__)

mysql = conexion.mysql



def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)

@cartaPedidos.route("/productosg/select/", methods = ["GET"])
def pedidosSelectG():
    resultado = []
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, imagen, descripcion, idCategoria FROM producto WHERE estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                categoria = {
                    "idProducto": fila[0],
                    "nombreProducto": fila[1],
                    "precio": fila[2],
                    "imagen": fila[3],
                    "descripcion": fila[4],
                    "idCategoria": fila[5]
                }
                resultado.append(categoria)
    except Exception as ex:
        resultado = "Ocurrio un error: " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@cartaPedidos.route("/productos/select/<string:name>/", methods = ["GET"])
def pedidosSelectID(name):
    resultado = []
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, imagen, descripcion, p.idCategoria, c.nombreCategoria FROM producto AS p INNER JOIN categoria AS c ON p.idCategoria = c.idCategoria WHERE p.estado = 1 AND c.nombreCategoria = %s;" 
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql,name)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                categoria = {
                    "idProducto": fila[0],
                    "nombreProducto": fila[1],
                    "precio": fila[2],
                    "imagen": fila[3],
                    "descripcion": fila[4],
                    "idCategoria": fila[5],
                    "nombreCategoria": fila[6],
                }
                resultado.append(categoria)
    except Exception as ex:
        resultado = "Ocurrio un error: " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

# este insert era para agregar el producto con todo y foto
# @cartaPedidos.route("/pedido/insert/", methods = ['POST'])
# def insertPedido():
#     try:
#         nombreProducto = request.form["txtnombreProducto"]
#         precioProducto = request.form["txtprecio"]
#         imagenProducto = request.files["txtimagen"]
#         descripProducto = request.form["txtdescripcion"]
#         catProducto = request.form["txtidCategoria"]
        
#         now = datetime.now()
#         tiempo = now.strftime("%Y%H%M%S")
#         mensaje = ""
#         datos = [
#             nombreProducto,
#             precioProducto,
#             descripProducto,
#             catProducto
#         ]
#         if imagenProducto.filename != '':
#             input_images_path = '\Repositorios/mibackEnd/upload/productos/'
#             cambioNombre = tiempo+imagenProducto.filename
#             sql = "INSERT INTO  (nombreProducto, precio, descripcion, idCategoria) VALUES (%s, %s, %s, %s, %s);"
#             # sql = "INSERT INTO misfotos (foto) VALUES (%s);"
#             conn = mysql.connect()
#             cursor = conn.cursor()
#             cursor.execute(sql, (datos,cambioNombre))
#             conn.commit()
#             imagenProducto.save(input_images_path + cambioNombre)
#             # cursor.execute(sql, (datos,(input_images_path + cambioNombre)))
#             mensaje ="foto guardada"
#         # descripProducto = request.form["txtdescripcion"]
#         # catProducto = request.form["txtidCategoria"]
#         # nombreProducto = strip_tags(nombreProducto)
#         # precioProducto = strip_tags(precioProducto)
#         # descripProducto = strip_tags(descripProducto)
#         else:
#             mensaje ="foto NO guardada->"+str(imagenProducto)
#     except Exception as ex:
#         mensaje = "falla: " + repr(ex)
#     return jsonify({"mensaje": mensaje})


@cartaPedidos.route("/pedido/foto/<string:imagen>/", methods = ['GET'])
def cargarImagen(imagen):
    image_data = open('\Repositorios/mibackEnd/upload/productos/'+imagen, "rb").read()
    resultado = make_response(image_data)
    resultado.headers['Content-Type'] = 'image/png'
    return resultado

@cartaPedidos.route("/datosCarritoPedido/", methods = ['POST'])
def insertPedido():
    try:
        resultadoPedido = []
        resultadoDetallePedido = []
        print("antes del output")
        output = request.get_json()
        print(output)
        # print(type(output))
        output = json.loads(output)
        # print(output)
        # print(type(output))
        for key in output:
            print(key)
            # if key == "precio" or key == "idEmpleado" or key == "nombreCliente":
            resultadoPedido.append(output[key])
            # else:
            #     resultadoDetallePedido.append(output[key])
        print("resultado resultadoPedido es:")
        print(resultadoPedido)
        print("id empleado",resultadoPedido[3])
        # print("resultado resultadoDetallePedido es:")
        # print(resultadoDetallePedido)
        sql = "INSERT INTO pedido(costoTotal,idEmpleado,nombreCliente)VALUES(%s, %s, %s);"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, (resultadoPedido[1], resultadoPedido[3], resultadoPedido[4]))
        conn.commit()
        # print("antes de la consulta")
        sql2 = "SELECT idPedido FROM pedido WHERE idEmpleado = %s ORDER BY 1 DESC LIMIT 1;"
        conn2 = mysql.connect()
        cursor2 = conn2.cursor()
        cursor2.execute(sql2, resultadoPedido[3])
        dato = cursor2.fetchone()
        print("EL CURSOR ME DIO: ", dato[0])
        print("DATOS PARA LA CONSULTA inserpedido: ", resultadoPedido[1], resultadoPedido[3], resultadoPedido[4])
        print("DATOS PARA LA CONSULTA insertDetallepedido: ", dato[0], resultadoPedido[0], resultadoPedido[5], resultadoPedido[2])
        sql2 = "INSERT INTO detallepedido (idPedido, idProducto, cantidad, CostoDetalle) VALUES ( %s, %s, %s, %s);"
        conn2 = mysql.connect()
        cursor2 = conn2.cursor()
        cursor2.execute(sql2, (dato[0], resultadoPedido[0], resultadoPedido[5], resultadoPedido[1]))
        conn2.commit()
        mensaje = "el mensaje a llegado :)"
    except Exception as ex:
        mensaje = "falla: " + repr(ex)
    return jsonify({"mensaje": mensaje})
