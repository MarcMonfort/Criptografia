from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


with open("./2020_09_25_10_32_42_marc.monfort.key", "rb") as key:
    with open("./2020_09_25_10_32_42_marc.monfort.enc", "rb") as ciphertext:
        with open('./sol_AES_1', 'wb') as sol:

            #ECB
            # aes = AES.new(key.read(), AES.MODE_ECB)
            # sol.write(aes.decrypt(ciphertext.read()))

            #CBC_1       
            # aes = AES.new(key.read(), AES.MODE_CBC)
            # sol.write(aes.decrypt(ciphertext.read()))

            #CBC_2       
            # vi = ciphertext.read(16)
            # aes = AES.new(key.read(), AES.MODE_CBC, vi)
            # sol.write(aes.decrypt(ciphertext.read()))

            #CTR_1
            # aes = AES.new(key.read(), AES.MODE_CTR)
            # sol.write(aes.decrypt(ciphertext.read()))

            #CFB_1
            # aes = AES.new(key.read(), AES.MODE_CFB)
            # sol.write(aes.decrypt(ciphertext.read()))

            #CFB_2 CORRECTE
            vi = ciphertext.read(16)
            aes = AES.new(key.read(), AES.MODE_CFB, vi)
            x = aes.decrypt(ciphertext.read())
            y = unpad(x, AES.block_size)

            sol.write(y)