# para evitar inyecciones html usaremos la libreria re
import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection
conexion = Connection()
empleados = Blueprint("empleados", __name__)
mysql = conexion.mysql

# LISTO
@empleados.route("/empleados/select/", methods=["GET"])
def empleadoSel():
    resultado = []
    exito = True
    try:
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = 2;"
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo != 1 AND estado = 1;"
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
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "encuestasRealizadas": fila[3],
                    "estado": fila[4],
                    "idCargo": fila[5]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@empleados.route("/admins/select/", methods=["GET"])
def empleadoAdminSel():
    resultado = []
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = 1;"
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
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "encuestasRealizadas": fila[3],
                    "estado": fila[4],
                    "idCargo": fila[5],
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


# LISTO
@empleados.route("/empleados/get/<int:id>/", methods=["GET"])
def empleadoGet(id):
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idEmpleado=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                "encuestasRealizadas": dato[3],
                "estado": dato[4],
                "idCargo": dato[5],
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@empleados.route("/empleados/delete/<int:id>/", methods=["DELETE"])
def empleadoDelete(id):
    try:
        sql = "DELETE FROM empleado WHERE idEmpleado=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        conector.commit()
        mensaje = "El metodo delete se ha ejecutado exitosamente"
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el empleado"
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})

# MI SELECT DEBE DE TENER PARA AUQELLOS QUE EL ESTADO SEA 1(OSEA ACTIVO)
# LISTO
def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)
@empleados.route("/empleados/create/", methods=["POST"], defaults={"id": None})
# def empleadoCreateUpdate(id):
def empleadoInsert(id):
    try:
        # estana con comilla dobles pero le pondre una
        nombreEmpleado = request.form["txtnombreEmpleado2"]
        correoEmpleado = request.form["txtcorreoEmpleado2"]
        passwordEmpleado = request.form["txtpasswordEmpleado2"]
        encuestasRealizadas = request.form["txtencuestasRealizadas2"]
        idCargo = request.form["txtidCargo2"]
        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)
        passwordEmpleado = strip_tags(passwordEmpleado)
        datos = [
            nombreEmpleado,
            correoEmpleado,
            passwordEmpleado,
            encuestasRealizadas,
            idCargo,
        ]
        mensaje = ""
        sql = ""
        if id == None:
            if len(nombreEmpleado) >= 3 :
                cargosInsert= []
                sqlAux = ("SELECT idCargo FROM cargo WHERE idCargo =%s AND estado = 1;")
                # print(idCargo)
                conector = mysql.connect()
                cursor2 = conector.cursor()
                cursor2.execute(sqlAux,idCargo)
                cargosInsert = cursor2.fetchall()
                if len(cargosInsert)!= 0:
                    sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, encuestasRealizadas, idCargo) VALUES(%s, %s, AES_ENCRYPT(%s,'fer'), %s, %s);"
                    mensaje = "Insertado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})


@empleados.route("/empleados/update/<int:id>/", methods=["PUT"])
def empleadoCreateUpdate(id):
    try:
        nombreEmpleado = request.form["txtnombreEmpleado"]
        correoEmpleado = request.form["txtcorreoEmpleado"]
        passwordEmpleado = request.form["txtpasswordEmpleado"]
        encuestasRealizadas = request.form["txtencuestasRealizadas"]
        idCargo = request.form["txtidCargo"]
        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)
        passwordEmpleado = strip_tags(passwordEmpleado)
        datos = [
            nombreEmpleado,
            correoEmpleado,
            passwordEmpleado,
            encuestasRealizadas,
            idCargo,
        ]
        mensaje = ""
        sql = ""
        if passwordEmpleado == "":
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT AES_DECRYPT(passwordEmpleado, 'fer') FROM empleado WHERE idEmpleado=%s;",
                (id),
            )
            passwordEmpleado = cursor.fetchone()
            datos[2] = passwordEmpleado
        datos.append(id)
        sql = "UPDATE empleado SET nombreEmpleado = %s, correoEmpleado = %s, passwordEmpleado = AES_ENCRYPT(%s, 'fer'), encuestasRealizadas = %s, idCargo = %s WHERE idEmpleado=%s;"
        mensaje = "Actualizado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})

# CRUD DE LOS CARGOS
@empleados.route("/cargos/select/", methods=["GET"])
def cargosSel():
    resultado = []
    exito = True
    try:
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

@empleados.route("/cargos/get/<int:id>/", methods=["GET"])
def cargosGet(id):
    exito = True
    try:
        sql = "SELECT idCargo, nombreCargo FROM cargo WHERE idCargo=%s;"
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
    
@empleados.route("/cargos/create/", methods=["POST"], defaults={"id": None})
def cargosInsert(id):
    try:
        nombreCargo = request.form["txtnombreCargo"]
        nombreCargo = strip_tags(nombreCargo)
        datos = [
            nombreCargo
        ]
        mensaje = ""
        sql = ""
        if id == None:
            sql = "INSERT INTO cargo(nombreCargo) VALUES(%s);"
            mensaje = "Insertado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})

@empleados.route("/cargos/update/<int:id>/", methods=["PUT"])
def cargosUpdate(id):
    try:
        nombreCargo = request.form["txtnombreCargo2"]
        nombreCargo = strip_tags(nombreCargo)
        datos = [
            nombreCargo,
        ]
        datos.append(id)
        mensaje = ""
        sql = ""
        sql = "UPDATE cargo SET nombreCargo = %s WHERE idCargo=%s;"
        mensaje = "Actualizado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})

@empleados.route("/cargos/update2/<int:id>/", methods=["PUT"])
def cargosDeshabilitado(id):
    try:
        datos =[]
        datos.append(id)
        if id !=1 :
            sql = "UPDATE cargo SET estado = 2 WHERE idCargo=%s;"
            conector = mysql.connect()
            cursor = conector.cursor()
            cursor.execute(sql, id)
            conector.commit()
            mensaje = "El metodo delete se ha ejecutado exitosamente"
            exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el empleado"
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})