from Crypto.PublicKey import RSA
from Crypto.Util import number
from subprocess import run
import math

# Genera todos los archivos intermedios y el fichero desencriptado

def solve_quadratic(a, b, c):
    dis = (b**2) - (4*a*c)
    s1 = (-b - math.isqrt(dis)) // (2*a)
    s2 = (-b + math.isqrt(dis)) // (2*a)
    return (s1, s2)


with open("./marc.monfort_pubkeyRSA_pseudo.pem", 'r') as file:
    my_key = RSA.import_key(file.read())


# PRE-CONDITION
# p = r||s
# q = s||r
# #bits(r) = #bits(s) = 1/2#bits(p) = 1/2#bits(q)

# modulus -> ACB 
# #bits(A) == #bits(B) == #bits(modulus)/4
# #bits(C) == #bits(modulus)/2


num_bits = my_key.n.bit_length()//4  # bits(r) = #bits(s) = ...
carry_bit = 0 # can be 0, 1 or 2

while True:
    mask = (1 << num_bits) - 1
    B = my_key.n & mask

    A = my_key.n >> (3*num_bits)
    A -= carry_bit

    AB = (A << num_bits) + B    # eq. r*s
    rs = AB

    BA = (B << num_bits) + A
    C = (my_key.n >> num_bits) & ((mask << num_bits) + mask)    # central part
    C += (1 << (2*num_bits))*carry_bit

    r_s2 = (C - BA) + 2*AB
    r_s = math.isqrt(r_s2)    # eq. r+s

    if r_s**2 == r_s2:
        break
    elif carry_bit == 2:
        raise Exception("Pre-requisit incorrect!")

    carry_bit += 1


(r, s) = solve_quadratic(1, r_s, rs)

factor1 = (abs(r) << num_bits) + (abs(s))
factor2 = (abs(s) << num_bits) + (abs(r))

modulus = my_key.n
publicExponent = my_key.e
phiModulus = (factor1-1) * (factor2-1)
privateExponent = number.inverse(publicExponent, phiModulus)
if (privateExponent < 0):
    privateExponent += phiModulus

rsa_components = (modulus, publicExponent, privateExponent, factor1, factor2)
privateKey = RSA.construct(rsa_components)

# creating PEM file
with open("./prikeyRSA_pseudo.pem", 'wb') as file:
    file.write(privateKey.export_key('PEM'))


# executing openssl commands:
# openssl rsautl -decrypt -inkey prikeyRSA_pseudo.pem -in marc.monfort_RSA_pseudo.enc -out keyAES_pseudo.txt
# openssl enc -d -aes-128-cbc -pbkdf2 -kfile keyAES_pseudo.txt -in marc.monfort_AES_pseudo.enc -out decrypted_pseudo

run(['openssl', 'rsautl', '-decrypt', '-inkey', 'prikeyRSA_pseudo.pem',
     '-in', 'marc.monfort_RSA_pseudo.enc', '-out', 'keyAES_pseudo.txt'])

run(['openssl', 'enc', '-d', '-aes-128-cbc', '-pbkdf2', '-kfile',
     'keyAES_pseudo.txt', '-in', 'marc.monfort_AES_pseudo.enc', '-out', 'decrypted_pseudo'])


# copyright Marc Monfort