#!/bin/sh

CURDIR=$(realpath .)

if [ ${#} -eq 2 ]; then
  user="${1}" && password="${2}"
elif [ ${#} -eq 1 ]; then
  user="${1}"
  printf 'Password: ' && read password
else
  printf 'User: ' && read user
  printf 'Password: ' && read password
fi

printf '%s:' "${user}" >> "${CURDIR}/nginx/htpasswd"
openssl passwd -apr1 >> "${CURDIR}/nginx/htpasswd"
