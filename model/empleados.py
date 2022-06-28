from flask import Blueprint, jsonify, request
from util.Connection import Connection
conexion = Connection()
empleados = Blueprint("empleados", __name__)
mysql = conexion.mysql

# LISTO
@empleados.route("/empleados/select/", methods=["GET"])
def empleadoSel():
    print("estoy en empleados")
    resultado = []
    exito = True
    try:
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, passwordEmpleado, imagen, encuestasRealizadas, estado, idCargo FROM empleado"
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = 2;"
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
                    # "passwordEmpleado": fila[3],
                    # "imagen": fila[4],
                    "encuestasRealizadas": fila[3],
                    "estado": fila[4],
                    "idCargo": fila[5],
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
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, passwordEmpleado, imagen, encuestasRealizadas, estado, idCargo FROM empleado"
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
                    # "passwordEmpleado": fila[3],
                    # "imagen": fila[4],
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
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, passwordEmpleado, imagen, encuestasRealizadas, estado, idCargo FROM empleado WHERE idEmpleado=%s"
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idEmpleado=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()  # None
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                # "passwordEmpleado": dato[3],
                # "imagen": dato[4],
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


# NO SE QUE ES ESTO, CREO QUE PARA EL PANDA
# @empleados.route("/empleados/crear/", methods=["POST"])
# def empleadoIns():
#     sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, imagen, encuestasRealizadas, estado, idCargo) VALUES(%s,%s,%s,%s,%s,%s,%s)"
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     request_data = request.get_json()
#     arreglo = request_data
#     for elemento in arreglo:
#         cursor.execute(sql, elemento)
#     conn.commit()
#     return jsonify(arreglo)

# MI SELECT DEBE DE TENER PARA AUQELLOS QUE EL ESTADO SEA 1(OSEA ACTIVO)
# LISTO
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
            # print("estamos en el IF")
            # sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, imagen, encuestasRealizadas, estado, idCargo) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, encuestasRealizadas, idCargo) VALUES(%s, %s, AES_ENCRYPT(%s,'fer'), %s, %s);"
            # sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, encuestasRealizadas, idCargo VALUES('fer', 'ferhotmail', AES_ENCRYPT('8', 'fer'),  80,  1)"
            mensaje = "Insertado correctamente"
        # else:
        #     # print("estamos en el ELSE")
        #     # si la contraseña esta vacia, realizamos una consulta, la desencriptamos y luego la reutilizamos para actualizar los datos
        #     if passwordEmpleado == "":
        #         conn = mysql.connect()
        #         cursor = conn.cursor()
        #         print("contraseña vacia:", passwordEmpleado)
        #         cursor.execute(
        #             "SELECT AES_DECRYPT(passwordEmpleado, 'fer') FROM empleado WHERE idEmpleado=%s;", (id)
        #         )
        #         passwordEmpleado = cursor.fetchone()
        #         datos[2]=passwordEmpleado
        #         print("la contra es:", passwordEmpleado)
        #     datos.append(id)
        #     sql = "UPDATE empleado SET nombreEmpleado = %s, correoEmpleado = %s, passwordEmpleado = AES_ENCRYPT(%s, 'fer'), encuestasRealizadas = %s, idCargo = %s WHERE idEmpleado=%s"
        #     mensaje = "Actualizado correctamente"
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
        # estana con comilla dobles pero le pondre una
        nombreEmpleado = request.form["txtnombreEmpleado"]
        correoEmpleado = request.form["txtcorreoEmpleado"]
        passwordEmpleado = request.form["txtpasswordEmpleado"]
        encuestasRealizadas = request.form["txtencuestasRealizadas"]
        idCargo = request.form["txtidCargo"]
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
            # print("contraseña vacia:", passwordEmpleado)
            cursor.execute(
                "SELECT AES_DECRYPT(passwordEmpleado, 'fer') FROM empleado WHERE idEmpleado=%s;",
                (id),
            )
            passwordEmpleado = cursor.fetchone()
            datos[2] = passwordEmpleado
            print("la contra es:", passwordEmpleado)
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