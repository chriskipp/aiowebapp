#!/bin/sh
#==================================================

PGDATA='/var/lib/postgresql/13/main'
SSL_CERT_FILE="${PGDATA}/server.crt"
SSL_KEY_FILE="${PGDATA}/server.key"
SSL_CA_FILE="${PGDATA}/root.crt"
SSL_CRL_FILE="${PGDATA}/root.key"

SERVER_CERTIFICAT="${PGDATA}/server.csr"
SERVER_KEY="${PGDATA}/server.key"

DOMAIN="/CO=db.domain.io"
#==================================================
[ -d "${PGDATA}" ] || mkdir --parents "${PGDATA}"

#[ -d nginx/ssl/certs ] || mkdir --parents nginx/ssl/certs
#[ -d nginx/ssl/private ] || mkdir --parents nginx/ssl/private

#==================================================
# Generating Certificate + Key
#==================================================
openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
	-out    "${SSL_CERT_FILE}" \
	-keyout "${SSL_KEY_FILE}" \

chmod og-rwx    "${SSL_KEY_FILE}"

#openssl dhparam -out "${PGDATA}/dhparam.pem" 4096


#==================================================
# Create Signing Request
#==================================================
openssl req -new -nodes -text \
	-out    "${SSL_CA_FILE}" \
	-keyout "${SSL_CRL_FILE}"

chmod og-rwx    "${SSL_CRL_FILE}"


#==================================================
# Signing Certificate
#==================================================
openssl x509 -req -in root.csr -text \
  -days 3650 \
  -extfile /etc/ssl/openssl.cnf \
  -extensions v3_ca \
  -signkey "${SSL_CRL_FILE}" \
  -out "${SSL_CRL_FILE}"

#==================================================
# Create Server Certificat signed by new root authhority
#==================================================
openssl req -new -nodes -text \
  -out    "${SERVER_CERTIFICAT}" \
  -keyout "${SERVER_KEY}" \
  -subj   "${DOMAIN}"

chmod og-rwx "${SERVER_KEY}"

#==================================================
# root.crt - Store on client to veryfy server
# root.key - Store offline to generate future certs
#==================================================
openssl x509 -req \
  -in "${SERVER_CERTIFICAT}" \
  -text -days 365 \
  -CA ./root.crt \
  -CAkey ./root.key \
  -CAcreateserial \
  -out "${SSL_CERT_FILE}" 

