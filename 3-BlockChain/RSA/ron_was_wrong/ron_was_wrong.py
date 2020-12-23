from Crypto.PublicKey import RSA 
from Crypto.Util import number
from subprocess import run
import os

# Genera todos los archivos intermedios y el fichero desencriptado

# Expliciacion:
# Como sabemos que alguna de las otras claves públicas de la carpeta "./RSA_RW-20201118"
# comparten un mismo factor que nuestra clave pública, podemos buscar el GCD entre
# el modulo de nuestra clave pública y el modulo de las otras claves publicas, y si 
# en efecto comparten factor, encontraremos el factor que sera diferente a 1
# y con ese primer factor encontraremos el segundo haciendo la division del modulo
# por el factor encontrado.
# Funciona porque encontrar el GCD es mucho más eficiente que factorizar

with open("./marc.monfort_pubkeyRSA_RW.pem",'r') as f:
    my_key = RSA.import_key(f.read())

directory = ("./RSA_RW-20201118")
for file_name in os.listdir(directory):
    if file_name.endswith(".pem"):
        file_path = (os.path.join(directory, file_name))
        with open(file_path,'r') as pem_file:
            other_key = RSA.import_key(pem_file.read())
            gcd = number.GCD(my_key.n, other_key.n)
            if gcd != 1 and gcd != my_key.n:
                factor1 = gcd
                break

factor2 = my_key.n // factor1

modulus = my_key.n
publicExponent = my_key.e
phiModulus = (factor1-1) * (factor2-1)
privateExponent = number.inverse(publicExponent, phiModulus)
if (privateExponent < 0):
    privateExponent += phiModulus


rsa_components = (modulus, publicExponent, privateExponent, factor1, factor2)
privateKey = RSA.construct(rsa_components)

with open("./prikeyRSA_RW.pem",'wb') as file:
    file.write(privateKey.export_key('PEM'))


# executing openssl commands:
# openssl rsautl -decrypt -inkey prikeyRSA_RW.pem -in marc.monfort_RSA_RW.enc -out keyAES_RW.txt
# openssl enc -d -aes-128-cbc -pbkdf2 -kfile keyAES_RW.txt -in marc.monfort_AES_RW.enc -out decrypted_RW

run(['openssl', 'rsautl', '-decrypt', '-inkey', 'prikeyRSA_RW.pem',
     '-in', 'marc.monfort_RSA_RW.enc', '-out', 'keyAES_RW.txt'])

run(['openssl', 'enc', '-d', '-aes-128-cbc', '-pbkdf2', '-kfile',
     'keyAES_RW.txt', '-in', 'marc.monfort_AES_RW.enc', '-out', 'decrypted_RW'])


# copyright Marc Monfort
