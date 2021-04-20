#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

wget 'http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2'
tar -xf parallel-latest.tar.bz2
subdir=$(tar -tf parallel-latest.tar.bz2 | grep --max-count=1 -o 'parallel-[0-9]*/')

(
  cd "${subdir}"
  ./configure && \
	make && \
	sudo make install
)

rm --force --recursive "${subdir}" parallel-latest.tar.bz2
cd -

printf 'will cite\n' | parallel --citation >/dev/null
