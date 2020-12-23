from Crypto.Util import number
import hashlib
import random
import pickle
from timeit import timeit


class rsa_key:
    def __init__(self, bits_modulo=2048, e=2**16+1):
        """ 
        genera una clau RSA (de 2048 bits i amb exponent públic 2**16+1 per defecte)
        """
        self.publicExponent = e

        while True:
            # genera 2 primos aleatorios de 1024 bits, coprimos con e
            self.primeP = number.getPrime(bits_modulo//2)
            self.primeQ = number.getPrime(bits_modulo//2)
            self.modulus = self.primeP * self.primeQ
            self.phiModulus = (self.primeP-1) * (self.primeQ-1)
            if (number.GCD(self.publicExponent, self.phiModulus) == 1):
                break

        self.privateExponent = number.inverse(
            self.publicExponent, self.phiModulus)
        if (self.privateExponent < 0):
            self.privateExponent += self.phiModulus

        self.privateExponentModulusPhiP = self.privateExponent % (
            self.primeP-1)  # d1
        self.privateExponentModulusPhiQ = self.privateExponent % (
            self.primeQ-1)  # d2

        self.inverseQModulusP = number.inverse(self.primeQ, self.primeP)  # q'
        self.Q_InverseQModulusP = self.primeQ * self.inverseQModulusP  # q*q'

    def sign(self, message):
        """ 
        retorma un enter que és la signatura de "message" feta amb la clau RSA fent servir el TXR
        """
        messageModulusP = message % self.primeP
        messageModulusQ = message % self.primeQ

        a = pow(messageModulusP, self.privateExponentModulusPhiP, self.primeP)
        b = pow(messageModulusQ, self.privateExponentModulusPhiQ, self.primeQ)

        return a*self.Q_InverseQModulusP + b*(1-self.Q_InverseQModulusP)

    def sign_slow(self, message):
        """ 
        retorma un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR
        """
        return pow(message, self.privateExponent, self.modulus)


class rsa_public_key:
    def __init__(self, rsa_key):
        """
        genera la clau pública RSA asociada a la clau RSA "rsa_key"
        """
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus

    def verify(self, message, signature):
        """
        retorna el booleà True si "signature" es correspon amb una
        signatura de "message" feta amb la clau RSA associada a la clau
        pública RSA.
        En qualsevol altre cas retorma el booleà False
        """
        return pow(signature, self.publicExponent, self.modulus) == message


class transaction:
    def __init__(self, message, RSAkey):
        """
        genera una transacció signant "message" amb la clau "RSAkey"
        """
        self.public_key = rsa_public_key(RSAkey)
        self.message = message
        self.signature = RSAkey.sign(message)

    def verify(self):
        """
        retorna el booleà True si "signature" es correspon amb una
        signatura de "message" feta amb la clau pública "public_key".
        En qualsevol altre cas retorma el booleà False
        """
        return self.public_key.verify(self.message, self.signature)


def get_block_hash(block):
    """
    genera un hash que cumpla la condición de proof-of-work de un bloque,
    y devuelpe una tupla con el hash y el seed correpondiente, usando
    sha256
    """
    entrada = str(block.previous_block_hash)
    entrada = entrada+str(block.transaction.public_key.publicExponent)
    entrada = entrada+str(block.transaction.public_key.modulus)
    entrada = entrada+str(block.transaction.message)
    entrada = entrada+str(block.transaction.signature)

    condition = 2**(256-16)
    while True:
        seed = random.randint(0, 2**256)
        entrada_seed = entrada+str(seed)

        h = int(hashlib.sha256(entrada_seed.encode()).hexdigest(), 16)
        if (h < condition):
            return (h, seed)


class block:
    def __init__(self):
        """
        crea un bloc (no necesàriamnet vàlid)
        """
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None
        self.seed = None

    def genesis(self, transaction):
        """
        genera el primer bloc d’una cadena amb la transacció "transaction" que es caracteritza per:
        - previous_block_hash=0
        - ser vàlid
        """
        self.previous_block_hash = 0
        self.transaction = transaction
        (self.block_hash, self.seed) = get_block_hash(self)
        return self

    def next_block(self, transaction):
        """
        genera el següent block vàlid amb la transacció "transaction"
        """
        new_block = block()
        new_block.previous_block_hash = self.block_hash
        new_block.transaction = transaction
        (new_block.block_hash, new_block.seed) = get_block_hash(new_block)
        return new_block

    def verify_block(self):
        """
        Verifica si un bloc és vàlid:
        -Comprova que el hash del bloc anterior cumpleix las condicions exigides
        -Comprova la transacció del bloc és vàlida
        -Comprova que el hash del bloc cumpleix las condicions exigides
        Si totes les comprovacions són correctes retorna el booleà True.
        En qualsevol altre cas retorma el booleà False
        """
        condition = 2**(256-16)

        isVerified = True

        if (not self.previous_block_hash < condition):
            print('\t** previous_block_hash: proof-of-work rejected')
            isVerified = False

        if (not self.transaction.verify()):
            print('\t** transaction: rejected')
            isVerified = False

        if (not self.block_hash < condition):
            print('\t** block_hash: proof-of-work rejected')
            isVerified = False

        entrada = str(self.previous_block_hash)
        entrada = entrada+str(self.transaction.public_key.publicExponent)
        entrada = entrada+str(self.transaction.public_key.modulus)
        entrada = entrada+str(self.transaction.message)
        entrada = entrada+str(self.transaction.signature)
        entrada = entrada+str(self.seed)
        h = int(hashlib.sha256(entrada.encode()).hexdigest(), 16)

        if (h != self.block_hash):
            print('\t** block_hash: rejected')
            isVerified = False

        return isVerified


class block_chain:
    def __init__(self, transaction):
        """
        genera una cadena de blocs que és una llista de blocs,
        el primer bloc és un bloc "genesis" generat amb la transacció "transaction"
        """
        self.list_of_blocks = [block().genesis(transaction)]

    def add_block(self, transaction):
        """
        afegeix a la llista de blocs un nou bloc vàlid generat amb la transacció "transaction"
        """
        new_block = self.list_of_blocks[-1].next_block(transaction)
        self.list_of_blocks.append(new_block)

    def verify(self):
        """
        verifica si la cadena de blocs és vàlida:
        - Comprova que tots el blocs són vàlids
        - Comprova que el primer bloc és un bloc "genesis"
        - Comprova que per cada bloc de la cadena el següent és el correcte
        Si totes les comprovacions són correctes retorna el booleà True.
        En qualsevol altre cas retorma el booleà False i fins a quin bloc la cadena és válida
        """
        isVerified = True

        for i in range(len(self.list_of_blocks)):
            if not self.list_of_blocks[i].verify_block():
                print('*** block {}: verification rejected'.format(i))
                isVerified = False

            if i != len(self.list_of_blocks)-1:
                if self.list_of_blocks[i].block_hash != self.list_of_blocks[i+1].previous_block_hash:
                    print('*** blocks {}-{}: chain rejected'.format(i, i+1))
                    isVerified = False

        if self.list_of_blocks[0].previous_block_hash != 0:
            print('*** genesis: rejected')
            isVerified = False

        return isVerified


###
# guardar i obrir Pickle
###

def generate_random_block_chain(number_of_blocks, path_of_file):
    """
    generate a pickle random BlockChain  object, with 
    number_of_blocks blocks, and save a file with the 
    object in path_of_file
    """
    RSAkey = rsa_key()
    t = transaction(random.randint(0, 2**256), RSAkey)
    bc = block_chain(t)

    for _ in range(number_of_blocks-1):
        RSAkey = rsa_key()
        t = transaction(random.randint(0, 2**256), RSAkey)
        bc.add_block(t)

    with open(path_of_file, 'wb') as file:
        pickle.dump(bc, file)


def get_block_chain(path_of_file):
    """ 
    get a pickle blockChain object from the file path_of_file
    """
    with open(path_of_file, 'rb') as file:
        block = pickle.load(file)
        return block

###
# Taula Comparativa
###

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def test_sign_amb_TXR(RSAkey, messageList):
    for i in range(100):
        RSAkey.sign(messageList[i])

def test_sign_sense_TXR(RSAkey, messageList):
    for i in range(100):
        RSAkey.sign_slow(messageList[i])

def test_timeit(key_bits):
    RSAkey = rsa_key(bits_modulo=key_bits)
    messageList = [random.getrandbits(256) for _ in range(100)] # 256 strong AES key

    wrapped_amb_TXR = wrapper(test_sign_amb_TXR, RSAkey, messageList)
    wrapped_sense_TXR = wrapper(test_sign_sense_TXR, RSAkey, messageList)
    
    time_amb_TXR = timeit(wrapped_amb_TXR, number=10)
    time_sense_TXR = timeit(wrapped_sense_TXR, number=10)
    return (time_amb_TXR/10, time_sense_TXR/10)


def taula_comparativa():
    print('\nTemps necessari per signar 100 missatges (segons):\n')
    print('\t#bits-clau','\t(amb-TXR)','\t(sense-TXR)','\n')

    (t_amb_TXR, t_sense_TXR) = test_timeit(512)
    print('\t   512:', end='')
    print('\t\t', round(t_amb_TXR,4), end='')
    print('\t\t', round(t_sense_TXR,4))

    (t_amb_TXR, t_sense_TXR) = test_timeit(1024)
    print('\t  1024:', end='')
    print('\t\t', round(t_amb_TXR,4), end='')
    print('\t\t', round(t_sense_TXR,4))

    (t_amb_TXR, t_sense_TXR) = test_timeit(2048)
    print('\t  2048:', end='')
    print('\t\t', round(t_amb_TXR,4), end='')
    print('\t\t', round(t_sense_TXR,4))

    (t_amb_TXR, t_sense_TXR) = test_timeit(4096)
    print('\t  4096:', end='')
    print('\t\t', round(t_amb_TXR,4), end='')
    print('\t\t', round(t_sense_TXR,4))
