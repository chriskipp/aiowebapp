#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libncurses-dev

# Get the source code e.g.
git clone https://github.com/davenquinn/sadisplay.git
#git clone https://github.com/agronholm/sqlacodegen.git

# Configure, build and install the Package
(
  cd sadisplay
  python3 setup.py install --user
)

# Remove Source Files
rm --force --recursive "sadisplay"

# Configure, build and install the Package
#(
#  cd sqlacodegen
#  python3 setup.py install --user
#)

# Remove Source Files
#rm --force --recursive "sqlacodegen"
#cd -
