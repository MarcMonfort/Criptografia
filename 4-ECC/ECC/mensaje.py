import hashlib

preambulo = 64*'20'
preambulo += ''.join(format(ord(c),'x') for c in 'TLS 1.3, server CertificateVerify')
preambulo += '00'

with open("./men.bin", 'rb') as f:

    men384 = hashlib.sha384(f.read())
    m = preambulo + men384.hexdigest()
    mensaje = hashlib.sha256(bytes.fromhex(m))

    print('mensaje (hex):', mensaje.hexdigest())

