from flask import Blueprint, jsonify, request
from util.Connection import Connection
import pandas as pd

# GET para traer informacion de la base de datos
# POST para insertar informacion a la base de datos
# PUT para actualizar informacion de la base de datos
# DELETE para eliminar informacion de la base de datos

# CONNECTION
# MYSQL
# CONEXION A LA BASE DE DATOS

conexion = Connection()
curso = Blueprint("curso", __name__)
mysql = conexion.mysql


@curso.route("/curso/select/", methods=["GET"])
def cursoSel():
    resultado = []
    exito = True
    try:
        sql = "SELECT id, nombre, creditos FROM curso"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                curso = {"id": fila[0], "nombre": fila[1], "creditos": fila[2]}
                resultado.append(curso)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@curso.route("/curso/get/<int:id>/", methods=["GET"])
def cursoGet(id):
    exito = True
    try:
        sql = "SELECT id, nombre, creditos FROM curso WHERE id=%s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()  # None
        # dato = [18, Innovacion y transformacion digital, 2]
        if dato != None:
            resultado = {"id": dato[0], "nombre": dato[1], "creditos": dato[2]}
        else:
            resultado = "No se ha encontrado el curso"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@curso.route("/curso/delete/<int:id>/", methods=["DELETE"])
def cursoDelete(id):
    try:
        sql = "DELETE FROM curso WHERE id=%s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        conector.commit()
        mensaje = "El curso se ha eliminado exitosamente"
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el curso"
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})


@curso.route("/curso/crear/", methods=["POST"])
def cursoIns():
    sql = "INSERT INTO curso(nombre,creditos) VALUES(%s,%s)"
    conn = mysql.connect()
    cursor = conn.cursor()
    request_data = request.get_json()
    arreglo = request_data
    for elemento in arreglo:
        cursor.execute(sql, elemento)
    conn.commit()
    return jsonify(arreglo)


@curso.route("/curso/create/", methods=["POST"], defaults={"id": None})
@curso.route("/curso/update/<int:id>/", methods=["PUT"])
def cursoCreateUpdate(id):
    try:
        _nombre = request.form["txtNombre"]
        _creditos = request.form["txtCreditos"]
        datos = [_nombre, _creditos]
        mensaje = ""
        sql = ""
        if id == None:
            sql = "INSERT INTO curso(nombre,creditos) VALUES(%s,%s)"
            mensaje = "Insertado correctamente"
        else:
            datos.append(id)
            sql = "UPDATE curso SET nombre = %s, creditos = %s WHERE id=%s"
            mensaje = "Actualizado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})


@curso.route("/curso/cargarexcel/", methods=["POST"])
def obtenerExcel():
    # ExcelRegistro.xlsx
    _archivo = request.files["archivoExcel"]
    _archivo.save("upload/ " + _archivo.filename)
    # upload/ExcelRegistro.xlsx
    data = pd.read_excel("upload/" + _archivo.filename)
    arreglo = data.values.tolist()
    return jsonify({"cursos": arreglo})
