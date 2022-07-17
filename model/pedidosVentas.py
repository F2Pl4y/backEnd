import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection

conexion = Connection()
pedidos = Blueprint("pedidos", __name__)
mysql = conexion.mysql

@pedidos.route("/pedidos/select/", methods = ["GET"])
def pedidosSelect():
    resultado = []
    exito = True
    try:
        sql = "SELECT idCategoria, nombreCategoria FROM categoria WHERE idCategoria != 1"
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
                    "idCategoria": fila[0],
                    "nombreCategoria": fila[1]
                }
                resultado.append(categoria)
    except Exception as ex:
        resultado = "Ocurrio un error: " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})