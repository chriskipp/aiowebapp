#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libsqlite3-0 libsqlite3-dev libproj-dev libspatialite-dev libspatialindex-dev libspatialite7 libgeos-dev libgeos++-dev libfreexl-dev libreadosm-dev libxml2-dev libxml2-utils libminizip-dev


wget 'http://www.gaia-gis.it/gaia-sins/spatialite-tools-5.0.0.tar.gz'

# Evtl. unpack archives
tar -xf "spatialite-tools-5.0.0.tar.gz"

# Configure, build and install the Package
(
  cd "spatialite-tools-5.0.0"
  	./configure && \
  	make && \
  	sudo make install
)

# Remove Source Files
rm --force --recursive "spatialite-tools-5.0.0" "spatialite-tools-5.0.0.tar.gz"
cd -
