#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libncurses-dev

# Get the source code e.g.
git clone https://github.com/chriskipp/git-dot.git

# Evtl. unpack archives
# tar -xf software.tar.xz

# Configure, build and install the Package
(
  cd git-dot
  python3 setup.py install --user
)

# Remove Source Files
rm --force --recursive "git-dot"
cd -
