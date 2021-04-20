#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt install --yes libsqlite3-0 libsqlite3-dev libproj-dev libspatialite-dev libspatialindex-dev libspatialite7 libgeos-dev libgeos++-dev libfreexl-dev libreadosm-dev libxml2-dev libxml2-utils

wget 'http://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-5.0.0-beta0.tar.gz'

# Evtl. unpack archives
tar -xf 'libspatialite-5.0.0-beta0.tar.gz'

# Configure, build and install the Package
(
  cd 'libspatialite-5.0.0-beta0'
  	./configure && \
  	make && \
  	sudo make install
)

# Remove Source Files
rm --force --recursive 'libspatialite-5.0.0-beta0.tar.gz' 'libspatialite-5.0.0-beta0'
cd -
