#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

sudo apt update && sudo apt upgrade && \
	sudo apt-get install --yes libsqlite3-dev libreadline-dev libeditline-dev tcl tcl-dev

wget 'https://www.sqlite.org/src/tarball/sqlite.tar.gz'
tar -xf sqlite.tar.gz

(
  cd sqlite
  CFLAGS="-DSQLITE_ENABLE_COLUMN_METADATA=1" ./configure --enable-all --enable-tempstore --enable-threadsafe --enable-readline && \
	make && \
	#make test && \
	sudo make install
)

rm --force --recursive sqlite sqlite.tar.gz sqlite
cd -
