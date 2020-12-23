# Terminal
1. export SSLKEYLOGFILE="./keys.txt"
2. firefox &
3. sudo wireshark


# Wireshark
1. Preferencias -> Protocols -> TLS -> (Pre)-Master-Secret.. -> keys.txt
2. Empezar captura
3. firefox -> wikipedia.org
4. Finalizar captura


# Guardar
1. Hanshake Protocol: Clien Hello           -> 1.bin
2. Hanshake Protocol: Server Hello          -> 2.bin
3. Hanshake Protocol: Encrypted Extensions  -> 3.bin
4. Hanshake Protocol: Certificate           -> 4.bin


# Info
(HP = Hanshake Protocol)


## Hash
1. HP: Server Hello / Cipher Suite = Cipher Suite: TLS_AES_256_GCM_SHA384 (0x1302)
2. HASH =

    SHA384

(se aplicara a la concatenacion de las 4 partes)


## Clave Pública de Wikipedia / Punto de la curva Q = (Qx, Qy)
1. HP: Certificate / Certificates / Certificate (Wikimedia Foundation) / signedCertificate / subjectPublicKeyInfo / subjectPublicKey
2. subjectPublicKey = 

    04dedb39245f4d61ed2e9b2f892c9d2e7b9d56283c2e4feb71cf410839b825e15a175d2cb9e5def9e95e17028dd3e6a7a4b42542c4a98e134b4d0a50356e6f67b3

3. Puntos de la curva Q (32 bytes) (hex)

    04 -> no_comprimido
    Qx = dedb39245f4d61ed2e9b2f892c9d2e7b9d56283c2e4feb71cf410839b825e15a
    Qy = 175d2cb9e5def9e95e17028dd3e6a7a4b42542c4a98e134b4d0a50356e6f67b3


## Datos de la curva (Que curva se esta usando)
1. HP: Certificate Verify / Signature Algorithm: ecdsa_secp256r1_sha256 / Signature
2. curva usada

    ecdsa_secp256r1_sha256

    Curva elíptica = p256
    documentacion = NIST.FIPS.186-4.PDF (pagina 100/91)
        (prime) p = 2^256 – 2^224 + 2^192 + 2^96 – 1.
                p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
                n = 115792089210356248762697446949407573529996955224135760342422259061068512044369

                c = 7efba166 2985be94 03cb055c 75d4f7e0 ce8d84a9 c5114abc af317768 0104fa0d
                b = 5ac635d8 aa3a93e7 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e 27d2604b

                Gx = 6b17d1f2 e12c4247 f8bce6e5 63a440f2 77037d81 2deb33a0 f4a13945 d898c296
                Gy = 4fe342e2 fe1a7f9b 8ee7eb4a 7c0f9e16 2bce3357 6b315ece cbb64068 37bf51f5

                ANNA        NIST
                 p    <->    p
                 q    <->    n
              (Qx,Qy) <->    (Gx, Gy)



2. Signatura =

    3046022100c5581c8fc4087eb656a0bab9b11b835e535dfcf77100a85d4341f54806abc432022100a216e731445535e7f28b380674c3a40ec0398fd464ce1ca0534d76d1a66296bf

    30 -> Secuencia de Objetos
    46 -> Longitud (hexadecimal)

    02 -> Entero
    21 -> Longitud entero (hexadecimal)
    f1 = 00c5581c8fc4087eb656a0bab9b11b835e535dfcf77100a85d4341f54806abc432

    02 -> Entero
    21 -> Longitud entero
    f2 = 00a216e731445535e7f28b380674c3a40ec0398fd464ce1ca0534d76d1a66296bf

Ya tenemos todos los datos!

----------------------
# Info de Curvas Elipticas
p = primo
E : y² = x³ - 3x + b  (mod p)
P € E(Zp)  punto de la curva con coeficientes mod p
q = orden del punto P:  q*P = 0 (NULL)
    (es primo)

## Clave privada / clave publica
privada = r entero mod q
pública = Q = r*p (punto de la curva)

## Verificar firma

Firma = (f1, f2)

w1 = mensaje * f2^(-1) mod q
w2 = f1 * f2^(-1) mod q

(x0, y0) = w1*P + w2*Q  (punto de curva E)

Aceptar <=> x0 mod q = f1.

[P = punto público, Q = clave publica de Wikipedia]

## ¿Que hay que conocer?
1. Datos de la curva elíptica
2. Clave pública Q (punto de la curva) (Sí)
3. Firma (f1, f2)   (sí)
4. Mensaje que se ha firmado


## Mensaje (todo en hex) concatenacion de ...

[Preambulo]
1. 64 veces '20'
2. 'TLS 1.3, server CertificateVerify' 
    en ASCII puro y luego en hexadecimal
= '544 ... 679'
3. Un byte separador = '00'
[Fin de preambulo]

++ (en binario...)

4. HP: Client Hello
5. HP: Server Hello
6. HP: Encrypted Extension
7. HP: Certificate

Concatenar en un único fichero:
cat 1.bin 2.bin 3.bin 4.bin > men.bin

8. hash (sha384) del fichero men.bin
    men384 = sha384(men.bin)
    como una cadena hexadecimal

MENSAJE = sha256(preambulo + men384)
este es el mensaje que hay que firmar

# Verificar en SAGE

    p = (primo FIPS)
    a = -3
    b = (FIPS) 5ac635d8 aa3a93e7 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e 27d2604b

    E = EllipticCurve(Zmod(p), [a,b])

    [x,y] in E  //  True or False

    // si cierto ...
    
    P = E ([x,y])   //ahora P sí es un punto cierto de la curva

    // 5*P = P + P + P + P

    SAGE

    p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    a = -3
    b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

    E = EllipticCurve(Zmod(p), (a, b))

    # (b) Comproveu que la clau pública P de www.wikipedia.org és realment un punt de la corba.
    Px = 0xdedb39245f4d61ed2e9b2f892c9d2e7b9d56283c2e4feb71cf410839b825e15a
    Py = 0x175d2cb9e5def9e95e17028dd3e6a7a4b42542c4a98e134b4d0a50356e6f67b3

    [Px,Py] in E

    # (c) Calculeu l’ordre del punt P .
    P = E([Px,Py])
    P_order = P.order()
    # P_order = 115792089210356248762697446949407573529996955224135760342422259061068512044369

