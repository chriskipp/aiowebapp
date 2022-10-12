#!/bin/sh

[ -f nginx/dhparam.pem ] && rm -f nginx/dbparam.pem
find ssl -true -execdir rm {} \;

[ -d nginx/ssl/certs ] || mkdir --parents ssl/certs
[ -d nginx/ssl/private ] || mkdir --parents ssl/private

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/private/nginx-selfsigned.key -out ssl/certs/nginx-selfsigned.crt
openssl dhparam -out nginx/dhparam.pem 4096
