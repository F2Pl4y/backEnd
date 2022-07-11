# para evitar inyecciones html usaremos la libreria re
import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection
conexion = Connection()
empleados = Blueprint("empleados", __name__)
mysql = conexion.mysql

# INICIO DE FUNCIONES DENTRO DEL ENTORNO VIRTUAL
# bloquea las inyecciones html
def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)
# validacion1: valida el nombre y el cargo
def validacion1(nombreEmpleado, idCargo):
    valorBool = False
    # valida que el nombre tenga como minimo 3 caracteres
    if len(nombreEmpleado) >= 3 :
        cargosInsert= []
        sqlAux = ("SELECT idCargo FROM cargo WHERE idCargo = %s AND estado = 1;")
        conector = mysql.connect()
        cursor2 = conector.cursor()
        cursor2.execute(sqlAux, idCargo)
        cargosInsert = cursor2.fetchall()
        # valida si el id del cargo esta activo o no
        if len(cargosInsert)!= 0:
            valorBool = True
    return valorBool


def validacion4(idCargo):
    valorBool = False
    # valida que el nombre tenga como minimo 3 caracteres
    cargosInsert= []
    sqlAux = ("SELECT idCargo FROM cargo WHERE idCargo = %s AND estado = 1;")
    conector = mysql.connect()
    cursor2 = conector.cursor()
    cursor2.execute(sqlAux,idCargo)
    cargosInsert = cursor2.fetchall()
    # valida si el id del cargo esta activo o no
    if len(cargosInsert)!= 0:
        valorBool = True
    return valorBool
# validacion2: se valida el permiso para inhabilitar un cargo | lo voy a cambiar sobre si dentro del cargo hay empleados con ese id
def validacion2(id):
    valorBool = False
    cargosInsert = []
    sqlAux = ("SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = %s AND estado = 2;")
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
# FIN DE FUNCIONES

# LISTO
@empleados.route("/empleados/select/", methods=["GET"])
def empleadoSel():
    resultado = []
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo != 2 AND estado = 1;"
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
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo = 1 AND estado = 1;"
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, idCargo FROM empleado WHERE idCargo = 2 AND estado = 1;"
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
                    # "encuestasRealizadas": fila[3],
                    # "estado": fila[4],
                    "idCargo": fila[3]
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
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idEmpleado=%s AND estado = 1;"
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
                "idCargo": dato[5]
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@empleados.route("/empleadosXcargo/get/<int:id>/", methods=["GET"])
def empleadoXcargoGet(id):
    exito = True
    try:
        sql = "SELECT idEmpleado, idCargo,nombreEmpleado FROM empleado WHERE idEmpleado=%s AND estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "idCargo": dato[1],
                "nombreEmpleado": dato[2]
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
@empleados.route("/empleados/create/", methods=["POST"], defaults={"id": None})
# def empleadoCreateUpdate(id):
def empleadoInsert(id):
    try:
        # estana con comilla dobles pero le pondre una
        nombreEmpleado = request.form["txtnombreEmpleado2"]
        correoEmpleado = request.form["txtcorreoEmpleado2"]
        passwordEmpleado = request.form["txtpasswordEmpleado2"]
        # encuestasRealizadas = request.form["txtencuestasRealizadas2"]
        idCargo = request.form["txtidCargo2"]
        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)
        passwordEmpleado = strip_tags(passwordEmpleado)
        datos = [
            nombreEmpleado,
            correoEmpleado,
            passwordEmpleado,
            # encuestasRealizadas,
            idCargo
        ]
        mensaje = ""
        sql = ""
        if id == None:
            # valida que el nombre tenga como minimo 3 caracteres
            validacion = validacion1(nombreEmpleado, idCargo)
            if validacion == True:
            # if len(nombreEmpleado) >= 3 :
            #     cargosInsert= []
            #     sqlAux = ("SELECT idCargo FROM cargo WHERE idCargo =%s AND estado = 1;")
            #     conector = mysql.connect()
            #     cursor2 = conector.cursor()
            #     cursor2.execute(sqlAux,idCargo)
            #     cargosInsert = cursor2.fetchall()
            #     # valida si el id del cargo esta activo o no
            #     if len(cargosInsert)!= 0:
                # sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, encuestasRealizadas, idCargo) VALUES(%s, %s, AES_ENCRYPT(%s,'fer'), %s, %s);"
                sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, idCargo) VALUES(%s, %s, AES_ENCRYPT(%s,'fer'), %s);"
                mensaje = "Insertado correctamente"
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, datos)
                conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion empleados / create"
    return jsonify({"mensaje": mensaje})

@empleados.route("/empleados/update/<int:id>/", methods=["PUT"])
def empleadoCreateUpdate(id):
    try:
        nombreEmpleado = request.form["txtnombreEmpleado"]
        correoEmpleado = request.form["txtcorreoEmpleado"]
        passwordEmpleado = request.form["txtpasswordEmpleado"]
        idCargo = request.form["txtidCargo"]
        # validarContraseña = request.form["txtContraseñaAdmin"]
        # validarContraseña2 = validarContraseña
        # print("el ipcargo es: ",idCargo)
        # encuestasRealizadas = request.form["txtencuestasRealizadas"]
        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)
        passwordEmpleado = strip_tags(passwordEmpleado)
        sinespacios= nombreEmpleado.replace(' ', '')
        datos = [
            nombreEmpleado,
            correoEmpleado,
            passwordEmpleado,
            # encuestasRealizadas,
            idCargo
        ]
        mensaje = ""
        sql = ""
        if passwordEmpleado == "":
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT AES_DECRYPT(passwordEmpleado, 'fer') FROM empleado WHERE idEmpleado=%s;",
                (id)
            )
            passwordEmpleado = cursor.fetchone()
            datos[2] = passwordEmpleado
        # sqlAuxValidarContraseña = ("SELECT AES_DECRYPT(passwordEmpleado, 'fer') FROM empleado WHERE idEmpleado = %s;")
        # conector = mysql.connect()
        # cursor2 = conector.cursor()
        # cursor2.execute(sqlAuxValidarContraseña, id)
        # validarContraseña2 = cursor2.fetchone()
        # validarContraseña2 = [x.decode() for x in validarContraseña2]
        # validarContraseña2 = "".join(validarContraseña2)
        # valornuevo = "".join(validarContraseña2)
        # if type(datos[3]) == int:
        EsEntero = datos[3].isnumeric()
        EsSoloLetras = datos[0].isalpha()
        # EsSoloLetras = datos[0].isalnum()
        # if EsEntero == True and EsSoloLetras==True:
        # validar si las encuestas son un entero y que el nombre SOLO tenga letras
        # if EsEntero == True and sinespacios.isalpha()==True:
        valorValidacion = validacion1(nombreEmpleado, idCargo)
        datos.append(id)
        # print("el id es: ",id)
        # print("el tipo es:",type(datos[3]))
        # valorValidacion2 = validacion5(id)
        
        # print("la validacion de la contraseña : ",validarContraseña2)
        # print("la validacion de validarContraseña : ",validarContraseña)
        # print("el valor de idcargo es: ",idCargo)
        if valorValidacion == True:
            # if  validarContraseña == validarContraseña2:
            # sql = "UPDATE empleado SET nombreEmpleado = %s, correoEmpleado = %s, passwordEmpleado = AES_ENCRYPT(%s, 'fer'), encuestasRealizadas = %s, idCargo = %s WHERE idEmpleado=%s;"
            sql = "UPDATE empleado SET nombreEmpleado = %s, correoEmpleado = %s, passwordEmpleado = AES_ENCRYPT(%s, 'fer'), idCargo = %s WHERE idEmpleado=%s;"
            mensaje = "Actualizado correctamente"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, datos)
            conn.commit()
        else:
            mensaje = "no se actualizo"
    except Exception as ex:
        mensaje = "Error en la ejecucion empleados / update /"
    return jsonify({"mensaje": mensaje})

@empleados.route("/empleados/update2/<int:id>/", methods=["PUT"])
def empleadoCreateUpdate2(id):
    try:
        idCargo = request.form["micargonuevo"]
        nombreEmpleado = request.form["tituloModalCargoDes"]
        idCargo = strip_tags(idCargo)
        nombreEmpleado = strip_tags(nombreEmpleado)
        datos = [
            idCargo
        ]
        valorValidacion = validacion1(nombreEmpleado,idCargo)
        mensaje = ""
        sql = ""
        datos.append(id)
        if valorValidacion == True:
            sql = "UPDATE empleado SET idCargo = %s WHERE idEmpleado=%s;"
            mensaje = "Actualizado correctamente"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, datos)
            conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion empleados / update2 /"
    return jsonify({"mensaje": mensaje})


# CRUD DE LOS CARGOS
@empleados.route("/cargos/select/", methods=["GET"])
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

@empleados.route("/cargos/update/<int:id>/", methods=["PUT"])
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
        sql = "UPDATE cargo SET nombreCargo = %s WHERE idCargo=%s;"
        mensaje = "Actualizado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion cargos / update/"
    return jsonify({"mensaje": mensaje})

@empleados.route("/cargos/update2/<int:id>/", methods=["PUT"])
def cargosDeshabilitado(id):
    try:
        validacion = False
        resultado = []
        datos =[]
        datos.append(id)
        validacion = validacion2(id)
        if id !=1 :
            if (validacion == True):
                sql = "UPDATE cargo SET estado = 2 WHERE idCargo=%s;"
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
                sql = "UPDATE cargo SET estado = 1 WHERE idCargo=%s;"
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
@empleados.route("/EmpleadosXcargo/select/<int:id>/", methods=["GET"])
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
#abraham
@empleados.route("/empleados/loginget/<int:id>/", methods=["GET"])
def empleadoLoginGet(id):
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, e.estado, nombreCargo FROM empleado as e INNER JOIN cargo as c ON e.idCargo = c.idCargo WHERE idEmpleado=%s;"
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
                "nombreCargo": dato[5],
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@empleados.route('/empleados/login/', methods = ['POST'])
def loginCreate():
    exito = True
    try:
        _correo = request.form['txtCorreo']
        _correo = strip_tags(_correo)
        _password = request.form['txtPassword']
        _password = strip_tags(_password)
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, idCargo FROM empleado WHERE correoEmpleado = %s AND passwordEmpleado = AES_ENCRYPT(%s, 'fer');"
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, idCargo FROM empleado WHERE correoEmpleado = %s AND passwordEmpleado = AES_ENCRYPT(%s, %s);"
        conector = mysql.connect()
        cursor = conector.cursor()
        # cursor.execute(sql, (_correo, _password, _password))
        cursor.execute(sql, (_correo, _password))
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                "encuestasRealizadas": dato[3],
                "idCargo": dato[4]
            }
        else:
            resultado = "Usuario o contraseña incorrecta"
            exito = False
    except Exception as ex:
        exito = False
        resultado = "Ocurrio un error al consultar el empleado"
    return jsonify({'resultado':resultado, 'exito':exito}) 