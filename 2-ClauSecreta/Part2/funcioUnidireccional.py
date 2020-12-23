from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


hex32 = lambda V: "{0:032x}".format(V)

################
#  Modificant K
################

K = 0
def testK():
    M = 0x00112233445566778899AABBCCDDEEFF
    Mb = M.to_bytes(16,'big')
    maxZero = 0xffffffffffffffffffffffffffffffff
    global K
    while True:
        K += 1 #seq. way
        aes = AES.new(K.to_bytes(16,'big'), AES.MODE_ECB) #seq. way
        #K = get_random_bytes(16)
        #aes = AES.new(K, AES.MODE_ECB)
        C = int.from_bytes(aes.encrypt(Mb),'big')
        if C < maxZero:
            maxZero = C
            print(hex32(maxZero),'\tKey:',hex32(K),'\ti =',K)


testK()
""" best so far... 
0000000167b62b58454c62501f1cb30a 	Key: 000000000000000000000000308ff9ec 	i = 814741996
i=928555888
"""
################
#  Modificant M
################

C = 0x00000000000000000000000000000000
K = 0x0123456789ABCDEFFEDCBA9876543210 # fixed K
aes = AES.new(K.to_bytes(16,'big'), AES.MODE_ECB)
M = aes.decrypt(C.to_bytes(16,'big'))

print('\nModificant M','\nM:',M.hex())

""" 
Si desxifrem amb la clau K un bloc C amb tot 0,
podrem trobar una M, tal que al xifrar M amb K el resultat
són tot 0
 """


################
#  Modificant M i K
################

C = 0x00000000000000000000000000000000
K = get_random_bytes(16)
aes = AES.new(K, AES.MODE_ECB)
M = aes.decrypt(C.to_bytes(16,'big'))

print('\nModificant M i K (hex)','\nK:',K.hex(),'\nM:',M.hex())

""" 
Si desxifrem amb una clau qualsevol un bloc C amb tot 0,
podrem trobar una M, tal que al xifrar M amb K el resultat
són tot 0
 """


