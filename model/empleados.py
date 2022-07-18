# para evitar inyecciones html usaremos la libreria re
import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection

conexion = Connection()
empleados = Blueprint("empleados", __name__)
mysql = conexion.mysql

# INICIO DE FUNCIONES DENTRO DEL ENTORNO VIRTUAL

def ValidarSesionUpdate(id):
    # cargosInsert= []
    sqlAux = ("SELECT idEmpleado FROM empleado WHERE idEmpleado = %s AND estado = 1;")
    conector = mysql.connect()
    cursor2 = conector.cursor()
    cursor2.execute(sqlAux,(id))
    cargosInsert = cursor2.fetchone()
    cargosInsert = int(''.join(map(str, cargosInsert)))
    return cargosInsert
    # Se puede usar un while para el fetchone (NO BORRAR)
    # while cargosInsert is not None:
    #     print(cargosInsert)
    #     idSesion = cargosInsert
    #     cargosInsert = cursor2.fetchone()
# esto de aqui es de prueba, no sirve para el proyecto
# @empleados.route("/miid/<int:id>/", methods=["GET"])
# def obtenerID(id):
#     try:
#         valorID = ValidarSesionUpdate(id)
#         mensaje = ""
#         exito = True
#     except Exception as ex:
#         mensaje = "falla: "+repr(ex)
#         exito = False
#     return jsonify({"resultado": mensaje, "exito": exito})

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
# FIN DE FUNCIONES

# LISTO
@empleados.route("/empleados/select/", methods=["GET"])
def empleadoSel():
    resultado = []
    exito = True
    try:
        # sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, estado, idCargo FROM empleado WHERE idCargo != 1 AND estado = 1;"
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, e.estado, nombreCargo FROM empleado AS e INNER JOIN cargo AS c ON e.idCargo = c.idCargo WHERE e.idCargo != 1 AND e.estado = 1;"
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
                    "nombreCargo": fila[5]
                }
                    # "idCargo": fila[5]
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
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, idCargo FROM empleado WHERE idCargo = 1 AND estado = 1;"
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

# @empleados.route("/empleados/delete/<int:id>/", methods=["DELETE"])
@empleados.route("/empleados/delete/<int:id>/<int:id2>/", methods=["DELETE"])
# def empleadoDelete(id,inputValue):
def empleadoDelete(id,id2):
    try:
        print("valor del id", id)
        # mantener la validacion (quiza sirva mas adelante)
        # validarDelete = ValidarSesionUpdate(id)
        print("valor de id2", id2)
        if id != id2:
            sql = "DELETE FROM empleado WHERE idEmpleado=%s;"
            conector = mysql.connect()
            cursor = conector.cursor()
            cursor.execute(sql, id)
            conector.commit()
            mensaje = "El metodo delete se ha ejecutado exitosamente"
            exito = True
        else:
            # mensaje = "No puedes eliminar a este administrador si estas logeado con dicha cuenta"
            mensaje = "Estás conectado con esta cuenta, no puedes eliminarla"
            exito = False
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el empleado"
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})

# MI SELECT DEBE DE TENER PARA AUQELLOS QUE EL ESTADO SEA 1(OSEA ACTIVO)
# LISTO
@empleados.route("/empleados/create/", methods=["POST"], defaults={"id": None})
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
                sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, idCargo) VALUES(%s, %s, HEX(AES_ENCRYPT(%s,'claveFer')), %s);"
                mensaje = "Insertado correctamente"
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, datos)
                conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion empleados / create"
    return jsonify({"mensaje": mensaje})

def empleadoDeletePrueba(id):
    try:
        sqlAux22 = "SELECT AES_DECRYPT( UNHEX(passwordEmpleado), 'claveFer') FROM empleado WHERE idEmpleado = %s;"
        conector = mysql.connect()
        cursor2 = conector.cursor()
        cursor2.execute(sqlAux22,(id))
        cargosInsert = cursor2.fetchone()
        cargosInsert = [x.decode() for x in cargosInsert]
        cargosInsert = "".join(cargosInsert)
        mensaje = "cargosInsert: ",cargosInsert
        exito = True
        return cargosInsert
    except Exception as ex:
        mensaje = "falla: "+repr(ex)
        exito = False

@empleados.route("/empleados/update/<int:id>/", methods=["PUT"])
def empleadoCreateUpdate(id):
    try:
        nombreEmpleado = request.form["txtnombreEmpleado"]
        correoEmpleado = request.form["txtcorreoEmpleado"]
        passwordEmpleado = request.form["txtpasswordEmpleado"]
        idCargo = request.form["txtidCargo"]
        validarContraseña = request.form["txtContraseñaAdmin"]
        validarContraseña2 = validarContraseña
        # encuestasRealizadas = request.form["txtencuestasRealizadas"]
        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)
        passwordEmpleado = strip_tags(passwordEmpleado)
        sinespacios= nombreEmpleado.replace(' ', '')
        datos = [
            nombreEmpleado,
            correoEmpleado,
            passwordEmpleado,
            idCargo
        ]
        mensaje = ""
        sql = ""
        valorContraBD = "8888"
        valorContraBD2 = []
        valorContraBD2 = empleadoDeletePrueba(id)
        valorContraBD = "".join(valorContraBD2)
        if passwordEmpleado == "":
            datos[2] = empleadoDeletePrueba(id)
            valorContraBD2 = empleadoDeletePrueba(id)
            valorContraBD = "".join(valorContraBD2)
            mensaje = "dentro del if vacio passwordEmpleado == ""-->valor obtenido de valorContraBD: ", valorContraBD
        if sinespacios.isalpha()==True:
            valorValidacion = validacion1(nombreEmpleado, idCargo)
            datos.append(id)
            if valorValidacion == True:
                mensaje = "estoy dentro de valorValidacion == True | valor de validarContraseña", validarContraseña, "| valor de valorContraBD", valorContraBD
                if  (validarContraseña == valorContraBD):
                    sql = "UPDATE empleado SET nombreEmpleado = %s, correoEmpleado = %s, passwordEmpleado = HEX(AES_ENCRYPT(%s, 'claveFer')), idCargo = %s WHERE idEmpleado=%s;"
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql, datos)
                    conn.commit()
                    mensaje = "si llegaste hasta aqui es xq actualizaste bien---> validarContraseña", validarContraseña, "|valorContraBD ",valorContraBD
            else:
                mensaje = "no se actualizo"
    except Exception as ex:
        mensaje = "falla: ", repr(ex), "la contraseña es: ",validarContraseña, " y la cambiada valorContraBD es: ",valorContraBD
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
                "nombreCargo": dato[5]
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
        print("correo despues del tag: ", _correo)
        _password = request.form['txtPassword']
        _password = strip_tags(_password)
        print("contraseña despues del tag: ", _password)
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, encuestasRealizadas, idCargo FROM empleado WHERE correoEmpleado = %s AND AES_DECRYPT(UNHEX(passwordEmpleado), 'claveFer') = %s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        # cursor.execute(sql, (_correo, _password, _password))
        cursor.execute(sql, (_correo, _password))
        # cursor.execute(sql)
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
        print("FALLANDO EN: ",repr(ex))
        exito = False
        resultado = "Ocurrio un error al consultar el empleado"
    return jsonify({'resultado':resultado, 'exito':exito})