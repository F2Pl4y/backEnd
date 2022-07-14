from Crypto.Cipher import AES 
import binascii,os
import random, string

iv = os.urandom(16)
aes_mode = AES.MODE_CBC
key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
print(key)
encryptor = AES.new(key, aes_mode, iv)
def aes_encrypt(plaintext):
    plaintext = convert_to_16(plaintext)

    ciphertext = encryptor.encrypt(plaintext)
    return ciphertext

def convert_to_16(plaintext): #Overcome the drawback of plaintxt size which should be multiple of len(iv)
    add = 16 - (len(plaintext) % 16)
    return(plaintext + ' ' * add)


Encrypted = aes_encrypt('Jaisal ')
print("Encrypted message :",Encrypted)
