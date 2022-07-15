# 0x636F6E7472617365C3B16168657861646563696D616C
# sin unhex: 0x313233 
import re
try: 
    hexstring = "0x7761C194BA873414775BA47CB814BECE"
    # hexstring = []
    # hexstring = ["0x313233", "0x646173646173","0x617364617364","0x313233","0x61736466617364","0x7364617364", "0x636F6E7472617365C3B16168657861646563696D616C"]
    # print("si funciona le quitamos los valores: ", hexstring)
    hexstring = hexstring.removeprefix('0x')
    a_string = bytes.fromhex(hexstring)
    a_string = a_string.decode("utf-8")
    print(a_string)
    # for contraseñas in hexstring:
    #     contraseñas = contraseñas.removeprefix('0x')
    #     a_string = bytes.fromhex(contraseñas)
    #     a_string = a_string.decode("utf-8")
    #     print(a_string)
except Exception as ex:
    print("FALLANDO EN: ",repr(ex))
