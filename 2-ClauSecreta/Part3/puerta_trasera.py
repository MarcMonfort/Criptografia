import subprocess
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def gen_preMasterKey():
    for x in range(256):
        for y in range(256):
            yield x.to_bytes(1, 'big')*8 + y.to_bytes(1, 'big')*8


with open("./2020_09_25_10_32_42_marc.monfort.puerta_trasera.enc", "rb") as ciphertext:
        ciphertext = ciphertext.read()
        preMasterKey = gen_preMasterKey()
        while True:
            try:
                H = SHA256.new(data=next(preMasterKey)).digest()
                aes = AES.new(H[:16], AES.MODE_CBC, H[16:])
                plaintext = unpad(aes.decrypt(ciphertext), AES.block_size)
            except ValueError:
                pass
            else:
                sol = open('./sol_AES_2', 'wb')
                sol.write(plaintext)
                sol.close()
                if len(subprocess.check_output('file sol_AES_2', shell=True)) > 20:
                    print(H[:16], H[16:])
                    break

