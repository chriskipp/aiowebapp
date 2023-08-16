#!/bin/sh

COMMON_NAME="${HOST}.blub"
PASS="pass:abcd"

# alpine
POSTGRES_GUID="70"
# debian
#POSTGRES_GUID="999"

# Check if executed in postgres directory or base directory of the repository
(
  test $(basename "${PWD}") = "postgres" \
    && [ -d "../data/postgres" ]
) || mkdir -p "../data/postgres"

sudo chown "${USER}:${USER}" "../data/postgres"
cd "../data/postgres"

SSL_DIR=$(realpath './ssl')
LOG_DIR=$(realpath './log')

[ -d "${LOG_DIR}" ] || mkdir "${LOG_DIR}"

[ -d "${SSL_DIR}" ] && sudo rm -rf "${SSL_DIR}"

mkdir "${SSL_DIR}" \
  && cd "${SSL_DIR}"

# rm old certificate files if they exist
for f in server.key server.crt server.req privkey.pem; do
  [ -f "${f}" ] && sudo rm -f "${f}"
done

# generate the server.key and server.crt
openssl req -new -text -passout "${PASS}" -subj "/CN=${COMMON_NAME}" -out server.req
openssl rsa -in privkey.pem -passin "${PASS}" -out server.key
openssl req -x509 -in server.req -text -key server.key -out server.crt

# set postgres (alpine) user as owner of the server.key and permissions to 600
#==========================
#sudo chown server.key
#sudo chmod 644 server.key
#==========================
sudo chown "${POSTGRES_GUID}:${POSTGRES_GUID}" server.key
sudo chmod 0600 server.key

[ -f privkey.pem ] && rm privkey.pem


# generate dhparam file
openssl dhparam -out "${SSL_DIR}/dhparam.pem" 2048

sudo chown --recursive "${POSTGRES_GUID}:${POSTGRES_GUID}" "${SSL_DIR}" "${LOG_DIR}"

