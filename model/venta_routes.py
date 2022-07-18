import re
from flask import Blueprint, jsonify, request, make_response
from util.Connection import Connection

conexion = Connection()
ventas = Blueprint("ventas", __name__)
mysql = conexion.mysql

@ventas.route("/ventas/select/", methods=["GET"])
def ventasSelect():
    resultado = []
    exito = True
    try:
        sql = "SELECT idVenta, fecha, montoTotal FROM venta"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                venta = {
                    "idVenta": fila[0],
                    "fecha": fila[1],
                    "montoTotal": fila[2]
                }
                resultado.append(venta)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})