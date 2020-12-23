import matplotlib.pyplot as plt
from time import time
from timeit import timeit
import random

modul = 0x11d   # modul Practica
# modul = 0x11b   # modul AES


def prod_por_x(b):
    if b >= 0x80:  # b7 == 1
        return (b << 1) ^ modul
    else:
        return b << 1


def GF_product_p(a, b):
    prod = 0
    for i in range(8):
        if b % 2 != 0:
            aux = a
            for _ in range(i):
                aux = prod_por_x(aux)
            prod ^= aux
        b >>= 1
    return prod


def GF_es_generador(a):
    generats = set()
    producte_acumulat = 1
    for _ in range(255):    # tambien podria 254
        producte_acumulat = GF_product_p(a, producte_acumulat)
        generats.add(producte_acumulat)
    return (len(generats) == 255)  # 255 -> no repetits


exp_taula = {}
log_taula = {}

generador = 0x02


def GF_tables():
    producte_acumulat = 1
    for i in range(255):
        exp_taula[i] = producte_acumulat
        log_taula[producte_acumulat] = i
        producte_acumulat = GF_product_p(generador, producte_acumulat)


def GF_product_t(a, b):
    if (a == 0 or b == 0):
        return 0
    else:
        index = (log_taula[a]+log_taula[b]) % 255
        return exp_taula[index]


def GF_invers(a):
    if (a == 0):
        return 0
    index = (255-log_taula[a]) % 255
    return exp_taula[index]


## Atenció! És considerarà un error greu si:
## Si tot retorna True no hi ha cap error

# GF_product_p(a, b)!=GF_product_t(a, b) per algun parell (a, b)
def check1():
    for a in range(255):
        for b in range(255):
            if GF_product_t(a,b) != GF_product_p(a,b):
                return False
    return True

# GF_product_p(a, b)!=GF_product_p(b, a) per algun parell (a, b)
def check2():
    for a in range(255):
        for b in range(255):
            if GF_product_p(a,b) != GF_product_p(b,a):
                return False
    return True

# GF_product_t(a, b)!=GF_product_t(b, a) per algun parell (a, b)
def check3():
    for a in range(255):
        for b in range(255):
            if GF_product_t(a,b) != GF_product_t(b,a):
                return False
    return True

# GF product p(a, GF invers(a))!=1 per a!=0
def check4():
    for a in range(1,255):
        if GF_product_p(a,GF_invers(a)) != 1:
            return False
    return True


GF_tables()

print('check1', check1())
print('check2', check2())
print('check3', check3())
print('check4', check4())


test = """ 
for x in range(256):
    GF_product_{}(x,{}) 
"""

def testTime(hexNum, p_t):
    import_fun = 'from __main__ import GF_product_{}'.format(p_t)
    time = timeit(test.format(p_t,hexNum), import_fun, number=10000)
    return round(time,4)

def compTaula():
    print('\nTaula comparativa multiplicant els 256 possibles valors')
    print('\tGF_product_p','\tGF_product_t','\t(micro-seconds)')

    print(' 0x02:', end='')
    print('\t  ', testTime(0x02,'p'), end='')
    print('\t  ', testTime(0x02,'t'))

    print(' 0x03:', end='')
    print('\t  ', testTime(0x03,'p'), end='')
    print('\t  ', testTime(0x03,'t'))

    print(' 0x09:', end='')
    print('\t  ', testTime(0x09,'p'), end='')
    print('\t  ', testTime(0x09,'t'))

    print(' 0x0B:', end='')
    print('\t  ', testTime(0x0B,'p'), end='')
    print('\t  ', testTime(0x0B,'t'))

    print(' 0x0D:', end='')
    print('\t  ', testTime(0x0D,'p'), end='')
    print('\t  ', testTime(0x0D,'t'))

    print(' 0x0E:', end='')
    print('\t  ', testTime(0x0E,'p'), end='')
    print('\t  ', testTime(0x0E,'t'))


# grafica temps
def graphTemps():
    xPlot_1 = [0]
    yPlot_1 = [0]

    t0 = time()*10000
    for i in range(300):
        a = random.randrange(256)
        b = random.randrange(256)
        GF_product_p(a,b)
        xPlot_1.append((time()*10000)-t0)
        yPlot_1.append(i)

    xPlot = [0]
    yPlot = [0]

    t0 = time()*10000
    GF_tables()
    for i in range(300):
        a = random.randrange(256)
        b = random.randrange(256)
        GF_product_t(a,b)
        xPlot.append((time()*10000)-t0)
        yPlot.append(i)


    plt.plot(xPlot_1, yPlot_1)
    plt.xlim(0,max(xPlot))
    plt.title('GF_product_p')
    plt.xlabel('temps transcorregut (micro)s')
    plt.ylabel('operacions realitzades')
    plt.show()

    plt.plot(xPlot, yPlot)
    plt.title('GF_product_t')
    plt.xlabel('temps transcorregut (micro)s')
    plt.ylabel('operacions realitzades')
    plt.show()


