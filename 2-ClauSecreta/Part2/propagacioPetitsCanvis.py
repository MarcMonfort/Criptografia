from Crypto.Cipher import AES
from Crypto.Random.random import getrandbits
import matplotlib.pyplot as plt


def posOnes(b):
    l = []
    i = 0
    while b:
        if b % 2 == 1:
            l.append(i)
        b >>= 1
        i += 1
    return l


K = getrandbits(128)        # fixed K
M = getrandbits(128)        # fixed M

aes = AES.new(K.to_bytes(16, 'big'), AES.MODE_ECB)
C = aes.encrypt(M.to_bytes(16, 'big'))
C = int.from_bytes(C, 'big')

################
#  Modificant M
################

histNumBits = {}
histPosBits = {}


for i in range(128):
    Mi = M ^ (1 << i)
    Ci = int.from_bytes(aes.encrypt(Mi.to_bytes(16, 'big')), 'big')

    #histNumBits.append(bin(C ^ Ci).count('1'))
    numOnes = bin(C ^ Ci).count('1')
    if numOnes in histNumBits:
        histNumBits[numOnes] += 1
    else:
        histNumBits[numOnes] = 1

    listPosOnes = posOnes(C ^ Ci)

    for x in listPosOnes:
        if x in histPosBits:
            histPosBits[x] += 1
        else:
            histPosBits[x] = 1


plt.bar(histNumBits.keys(), histNumBits.values())
plt.xlim(xmin=0, xmax=128)
plt.title("Nombre de bits que canvien en modificar M")
plt.xlabel("nombre de bits diferents")
plt.show()

plt.bar(histPosBits.keys(), histPosBits.values())
plt.title("Posicions que canvien en modificar M")
plt.xlabel("posició del bit")
plt.ylabel("nombre de canvis")
plt.show()


################
#  Modificant K
################

histNumBits = {}
histPosBits = {}


for i in range(128):
    Ki = K ^ (1 << i)
    aes = AES.new(Ki.to_bytes(16, 'big'), AES.MODE_ECB)
    Ci = int.from_bytes(aes.encrypt(M.to_bytes(16, 'big')), 'big')

    numOnes = bin(C ^ Ci).count('1')
    if numOnes in histNumBits:
        histNumBits[numOnes] += 1
    else:
        histNumBits[numOnes] = 1

    listPosOnes = posOnes(C ^ Ci)

    for x in listPosOnes:
        if x in histPosBits:
            histPosBits[x] += 1
        else:
            histPosBits[x] = 1


plt.bar(histNumBits.keys(), histNumBits.values())
plt.xlim(xmin=0, xmax=128)
plt.title("Nombre de bits que canvien en modificar K")
plt.xlabel("nombre de bits diferents")
plt.show()

plt.bar(histPosBits.keys(), histPosBits.values())
plt.title("Posicions que canvien en modificar K")
plt.xlabel("posició del bit")
plt.ylabel("nombre de canvis")
plt.show()