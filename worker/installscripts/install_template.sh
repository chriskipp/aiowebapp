#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libncurses-dev

# Get the source code e.g.
# git clone https://github.com/tmux/tmux.git
# wget 'https://nodejs.org/latest'

# Evtl. unpack archives
# tar -xf software.tar.xz

# Configure, build and install the Package
(
  cd DIRECTORY
  #sh autogen.sh && \
  #	./configure && \
  #	make && \
  #	sudo make install
)

# Remove Source Files
rm --force --recursive "${DIRECTORY}"
cd -
