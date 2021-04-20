#!/bin/sh

[ -d ssl ] || mkdir --parents ssl

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/gotty.key -out ssl/gotty.crt -batch

#openssl dhparam -out ssl/dhparam.pem 4096
