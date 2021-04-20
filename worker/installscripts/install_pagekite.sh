#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Get the source code e.g.
curl -s https://pagekite.net/pk/ | sudo sh

