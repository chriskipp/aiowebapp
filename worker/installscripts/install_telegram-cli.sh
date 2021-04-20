#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libpython2-dev make libconfig9 liblua5.2-0 libjansson4

# Get the source code e.g.
git clone https://github.com/vysheng/tg.git

# Configure, build and install the Package
(
  cd tg
  ./configure
  make
)

# Remove Source Files
#rm --force --recursive "${DIRECTORY}"
#cd -
