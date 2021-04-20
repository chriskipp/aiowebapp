#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Get the source code e.g.
git clone https://github.com/andreafrancia/trash-cli

# Evtl. unpack archives
# tar -xf software.tar.xz

# Configure, build and install the Package
(
  cd trash-cli
  sudo python3 setup.py install
)

# Remove Source Files
sudo rm --force --recursive trash-cli
cd -

# Ensuring dependencies
#python3 -m pip install psutil
