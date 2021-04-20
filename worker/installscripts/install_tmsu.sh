#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libncurses-dev

# Get the code 
deburl="https://code.launchpad.net/~tmsu/+archive/ubuntu/ppa/+build/11193268/+files/tmsu_0.6.1-0~934~ubuntu16.04.1_amd64.deb"
wget "${deburl}"



# Install the Package
(
  deb=$(basename "${deburl}")
  sudo dpkg -i "${deb}"
  rm --force "${deb}"
)

# Remove Source Files
cd -
