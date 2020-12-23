1. www.fib.upc.edu
2. Candado
3. Connection Secure
4. More Information
5. View Certificate


1. CRL Endpoints (Certificate Rebocation List)
2. Descargar uno de los dos
   (ej.  http://crl3.digicert.com/TERENASSLCA3.crl)

OPENSSL
3. Transformar a ficher de texto
y asi poder ver lista de rebocados.


AIA - Donde haremos la pregunta del certificado
1. Authority Info (AIA) 
2. Descargar (http://cacerts.digicert.com/TERENASSLCA3.crt)
3. Pasarlo a formato .PEM



1. Pestaña Terena SSL CA 3
2. Descargar AIA (http://cacerts.digicert.com/DigiCertAssuredIDRootCA.crt)
3. Convertir a formato .PEM (OpenSSL)



OPENSSL
1. Enviar orden a http://ocsp.digicert.com/  
con los certificado transformados obtenidos

Devuelve respuesta (okay, o no_okay)




COMANDOS
openssl crl -inform DER -text -noout -in TERENASSLCA3.crl -out crl.txt

Conte 7112 certificats revokats



# CRT -> PEM
openssl x509 -inform DER -in TERENASSLCA3.crt -out outcert.pem -text
---


openssl ocsp -issuer chain.pem -cert wikipedia.pem -text -url http://ocsp.digicert.com

openssl ocsp -issuer chain.pem -cert upc.pem -url http://ocsp.digicert.com



openssl ocsp -issuer digicert.pem -cert terena.pem -url http://ocsp.digicert.com