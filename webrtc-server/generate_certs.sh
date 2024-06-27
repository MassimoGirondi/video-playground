openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -out cert.pem -keyout cert.key
openssl x509 -noout -in cert.pem -text
openssl x509 -pubkey -noout -in cert.pem

