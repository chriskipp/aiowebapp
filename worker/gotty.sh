#!/bin/sh

gotty --port 5556  --credential user:pass --random-url --tls --tls-crt ssl/gotty.crt --tls-key ssl/gotty.key --permit-write /bin/zsh
