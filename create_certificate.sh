#!/bin/sh

[ -d nginx/ssl/certs ] || mkdir --parents nginx/ssl/certs
[ -d nginx/ssl/private ] || mkdir --parents nginx/ssl/private

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/private/nginx-selfsigned.key -out nginx/ssl/certs/nginx-selfsigned.crt
openssl dhparam -out nginx/dhparam.pem 4096
