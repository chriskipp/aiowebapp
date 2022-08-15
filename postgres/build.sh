#!/bin/sh

SSLDIR='./ssl'

[ -d "${SSLDIR}" ] || mkdir "${SSLDIR}"
cd "${SSLDIR}"

# rm old server.key, server.crt, server.req and privkey.pem
for f in server.key server.crt server.req privkey.pem; do
  [ -f "${f}" ] && rm -f "${f}"
done

# generate the server.key and server.crt
openssl req -new -text -passout pass:abcd -subj /CN=localhost -out server.req
openssl rsa -in privkey.pem -passin pass:abcd -out server.key
openssl req -x509 -in server.req -text -key server.key -out server.crt

# set postgres (alpine) user as owner of the server.key and permissions to 600
#sudo chown 0:70 server.key
#sudo chmod 640 server.key

