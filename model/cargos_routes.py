import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection
conexion = Connection()
cargos = Blueprint("cargos", __name__)
mysql = conexion.mysql
# INICIO VALIDACIONES
# bloquea las inyecciones html
def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)

# validacion2: se valida el permiso para inhabilitar un Cargo | lo voy a cambiar sobre si dentro del Cargo hay empleados con ese id
def validacion2(id):
    valorBool = False
    cargosInsert = []
    sqlAux = ("SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = %s AND estado = 1;")
    conector = mysql.connect()
    cursor2 = conector.cursor()
    cursor2.execute(sqlAux,id)
    # valida si el id del cargo esta activo o no
    cargosInsert = cursor2.fetchall()
    # print("el tamaño de cargosInsert es:", len(cargosInsert))
    # print("cargosInsert es:", cargosInsert)
    if len(cargosInsert) == 0:
        valorBool = True
    else:
        valorBool = False
    return valorBool

# validacion3: corroborar que el nombre del cargo no este vacío
def validacion3(nombreCargo):
    valorBool = False
    if len(nombreCargo)>=3:
        valorBool = True
    return valorBool
# FIN VALIDACIONES
@cargos.route("/cargos/select2/", methods=["GET"])
def cargosSel2():
    resultado = []
    exito = True
    try:
        # sql = "SELECT * FROM cargo WHERE estado = 1 AND idCargo != 1;"
        sql = "SELECT * FROM cargo WHERE estado = 1 AND idCargo !=1;"
        # conectarme a la BD
        conector = mysql.connect()
        # almacenar informacion
        cursor = conector.cursor()
        # ejecutar la sentencia
        cursor.execute(sql)
        # me duelve la informacion para poder imprimirla en donde necesite, por ejemplo en la terminal con un print(datos)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                Datosempleados = {
                    "idCargo": fila[0],
                    "nombreCargo": fila[1],
                    "estado": fila[2]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@cargos.route("/cargos/select/", methods=["GET"])
def cargosSel():
    resultado = []
    exito = True
    try:
        # sql = "SELECT * FROM cargo WHERE estado = 1 AND idCargo != 1;"
        sql = "SELECT * FROM cargo WHERE estado = 1;"
        # conectarme a la BD
        conector = mysql.connect()
        # almacenar informacion
        cursor = conector.cursor()
        # ejecutar la sentencia
        cursor.execute(sql)
        # me duelve la informacion para poder imprimirla en donde necesite, por ejemplo en la terminal con un print(datos)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                Datosempleados = {
                    "idCargo": fila[0],
                    "nombreCargo": fila[1],
                    "estado": fila[2]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@cargos.route("/cargos/get/<int:id>/", methods=["GET"])
def cargosGet(id):
    exito = True
    try:
        sql = "SELECT idCargo, nombreCargo FROM cargo WHERE idCargo = %s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idCargo2": dato[0],
                "nombreCargo2": dato[1]
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})
    
@cargos.route("/cargos/create/", methods=["POST"], defaults={"id": None})
def cargosInsert(id):
    try:
        nombreCargo = request.form["txtnombreCargo"]
        nombreCargo = strip_tags(nombreCargo)
        datos = [
            nombreCargo
        ]
        mensaje = ""
        sql = ""
        validacion = validacion3(nombreCargo)
        if id == None:
            if validacion == True:
                sql = "INSERT INTO cargo(nombreCargo) VALUES(%s);"
                mensaje = "Insertado correctamente"
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, datos)
                conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion cargos/create/"
    return jsonify({"mensaje": mensaje})

@cargos.route("/cargos/update/<int:id>/", methods=["PUT"])
def cargosUpdate(id):
    try:
        nombreCargo = request.form["txtnombreCargo2"]
        nombreCargo = strip_tags(nombreCargo)
        datos = [
            nombreCargo
        ]
        datos.append(id)
        mensaje = ""
        sql = ""
        sql = "UPDATE cargo SET nombreCargo = %s WHERE idCargo = %s;"
        mensaje = "Actualizado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion cargos / update/"
    return jsonify({"mensaje": mensaje})

@cargos.route("/cargos/update2/<int:id>/", methods=["PUT"])
def cargosDeshabilitado(id):
    try:
        validacion = False
        resultado = []
        datos =[]
        datos.append(id)
        validacion = validacion2(id)
        if id !=1 :
            if (validacion == True):
                sql = "UPDATE cargo SET estado = 2 WHERE idCargo = %s;"
                conector = mysql.connect()
                cursor = conector.cursor()
                cursor.execute(sql, id)
                conector.commit()
                # mensaje = "el cargo se ha inhabilitado exitosamente"
                exito = True
            else:
                datos2 = []
                datos2 = EmpleadosXcargo(id)
                # print("los datos2 son: ",datos2)
                for fila in datos2:
                    Datosempleados = {
                        "idEmpleado": fila[0],
                        "nombreEmpleado": fila[1],
                        "correoEmpleado": fila[2],
                        "encuestasRealizadas": fila[3],
                        "estado": fila[4],
                        "idCargo": fila[5]
                    }
                    resultado.append(Datosempleados)
                sql = "UPDATE cargo SET estado = 1 WHERE idCargo = %s;"
                conector = mysql.connect()
                cursor = conector.cursor()
                cursor.execute(sql,id)
                conector.commit()
                exito = True
    except Exception as ex:
        mensaje = "El id se coloca con otro metodo"
        exito = False
    # return jsonify({"resultado": resultado, "exito": exito, "mensaje":mensaje})
    return jsonify({"resultado": resultado, "exito": exito, "cargo": id})

# me devuelve los valores de empleado
def EmpleadosXcargo(id):
    try:
        resultado = []
        exito = True
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = %s AND estado = 1;"
        # conectarme a la BD
        conector = mysql.connect()
        # almacenar informacion
        cursor = conector.cursor()
        # ejecutar la sentencia
        cursor.execute(sql, id)
        # me duelve la informacion para poder imprimirla en donde necesite, por ejemplo en la terminal con un print(datos)
        datos = cursor.fetchall()
        # print("los datos son", len(datos))
        if len(datos) == 0:
            Datosempleados = {
                "idEmpleado": 0,
                "nombreEmpleado": "0",
                "correoEmpleado": "0",
                "encuestasRealizadas": 0,
                "estado": 0,
                "idCargo": 0
            }
            resultado.append(Datosempleados)
            exito = True
            # resultado = "No existen datos en la tabla"
        else:
            for fila in datos:
                Datosempleados = {
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "encuestasRealizadas": fila[3],
                    "estado": fila[4],
                    "idCargo": fila[5]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta /empleado/selectX/"
        exito = False
    return datos

@cargos.route("/EmpleadosXcargo/select/<int:id>/", methods=["GET"])
def EmpleadosXcargoRoute(id):
    try:
        resultado = []
        exito = True
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = %s AND estado = 1;"
        # conectarme a la BD
        conector = mysql.connect()
        # almacenar informacion
        cursor = conector.cursor()
        # ejecutar la sentencia
        cursor.execute(sql, id)
        # me duelve la informacion para poder imprimirla en donde necesite, por ejemplo en la terminal con un print(datos)
        datos = cursor.fetchall()
        if len(datos) != 0:
            for fila in datos:
                Datosempleados = {
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "encuestasRealizadas": fila[3],
                    "estado": fila[4],
                    "idCargo": fila[5]
                }
                resultado.append(Datosempleados)
        else:
            resultado = "No existen datos en la tabla"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta / EmpleadosXcargo / select"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})
