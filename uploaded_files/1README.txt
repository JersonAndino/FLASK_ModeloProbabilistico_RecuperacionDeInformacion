GENERACION de llaves y solicitud de certificado:
openssl req -newkey dsa:dsaparams.pem -keyout dsakeyMaflaE.pem -new -days 365 -out dsareqMaflaE.pem

EXTRAER llaves publica y privada
openssl dsa -in dsakeyMaflaE.pem -aes128 -out dsaprivMaflaE.pem
openssl dsa -in dsakeyMaflaE.pem -out dsapubMaflaE.pem -outform PEM -pubout

PRINT llaves, privada y publica:
openssl dsa -text -inform PEM -in dsakeyMaflaE.pem
openssl dsa -text -inform PEM -in dsaprivMaflaE.pem
openssl dsa -text -inform PEM -pubin -in dsapubMaflaE.pem

CONVERTIR PEM ==> P12 (Para firmar PDF en Adobe):
openssl pkcs12 -export -out certMaflaE.p12 -in certMaflaE.pem -inkey dsakeyMaflaE.pem -passin pass:contrasenaPEM -passout pass:contrasenaP12

FIRMAR Informe y convertir la firma a Base64:
openssl dgst -sha256 -sign dsakeyMaflaE.pem -out informe.sha256 Informe.pdf
openssl base64 -in informe.sha256 -out informeb64.sha256

ENVIAR el informe y la firma en Base64

VERIFICAR firma digital
openssl base64 -d -in informeb64.sha256 -out sign.sha256
openssl dgst -sha256 -verify DSApubMaflaE.pem -signature sign.sha256 Informe.pdf
