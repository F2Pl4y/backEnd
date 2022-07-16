import re
# from flask import Blueprint, jsonify, request
# from util.Connection import Connection
# pruebas = Blueprint("pruebas", __name__)
# conexion = Connection()
# mysql = conexion.mysql

# @pruebas.route("/empleados33/update/<int:id>/", methods=["PUT"])
# def pruebaupdate(id):
#     try:
#         # hexstring = []
#         # hexstring = ["0x313233", "0x646173646173","0x617364617364","0x313233","0x61736466617364","0x7364617364", "0x636F6E7472617365C3B16168657861646563696D616C"]
#         # print("si funciona le quitamos los valores: ", hexstring)
#         # hexstring = "0x313233343536"

#         sqlAuxValidarContraseña = ("SELECT AES_DECRYPT( UNHEX(passwordEmpleado), 'claveFer') FROM empleado WHERE idEmpleado = 6;")
#         conector = mysql.connect()
#         cursor2 = conector.cursor()
#         cursor2.execute(sqlAuxValidarContraseña)
#         validarContraseña2 = cursor2.fetchone()
#         print(validarContraseña2)
#         hexstring = "0x6665726E616E646F313233"
#         hexstring = hexstring.removeprefix('0x')
#         a_string = bytes.fromhex(hexstring)
#         a_string = a_string.decode("utf-8")
#         print(a_string)
#         print(type(a_string))
#         print(a_string == 123456)
#         # for contraseñas in hexstring:
#         #     contraseñas = contraseñas.removeprefix('0x')
#         #     a_string = bytes.fromhex(contraseñas)
#         #     a_string = a_string.decode("utf-8")
#         #     print(a_string)
#     except Exception as ex:
#         print("FALLANDO EN: ",repr(ex))

hexstring = "0x31323334"
hexstring = hexstring.removeprefix('0x')
a_string = bytes.fromhex(hexstring)
a_string = a_string.decode("utf-8")
print(a_string)

