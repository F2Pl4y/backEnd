import re
from flask import Blueprint, jsonify, request, make_response
from util.Connection import Connection

conexion = Connection()
pedido = Blueprint("pedido", __name__)
mysql = conexion.mysql

@pedido.route("/pedido/selectEmp/<int:id>", methods=["GET"])
def pedidoEmpleado(id):
    resultado = []
    exito = True
    try:
        sql = "SELECT idPedido, nombreCliente, estado, costoTotal, idEmpleado, p.idVenta FROM pedido as p inner join venta as v on p.idVenta = v.idVenta WHERE v.fecha = curdate() and idEmpleado = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                venta = {
                    "idPedido": fila[0],
                    "nombreCliente": fila[1],
                    "estado": fila[2],
                    "costoTotal": fila[3],
                    "idEmpleado": fila[4],
                    "idVenta": fila[5]
                }
                resultado.append(venta)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})