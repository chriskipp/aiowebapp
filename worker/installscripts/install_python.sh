#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev python3-dev libffi-dev

# Get the source code e.g.
archive_url='https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz'
wget  "${archive_url}"

# Evtl. unpack archives
archive_file=$(basename "${archive_url}")
source_dir=$(basename --suffix=.tar.xz "${archive_url}")
tar -xf "${archive_file}"

# Configure, build and install the Package
(
  cd "${source_dir}"
  ./configure --enable-optimisations && \
  make && \
  sudo make install
)

# Remove Source Files
sudo rm --force --recursive "${source_dir}" "${archive_file}"
cd -

sudo python3 -m pip install --upgrade pip


sudo python3 -m pip install --upgrade ipython
