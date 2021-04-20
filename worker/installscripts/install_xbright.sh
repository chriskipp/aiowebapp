#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libncurses-dev

# Get the source code e.g.
git clone https://github.com/snobb/xbright

# Configure, build and install the Package
(
  cd xbright 
  make && sudo make install
)

# Remove Source Files
sudo rm --force --recursive "xbright"
cd -
