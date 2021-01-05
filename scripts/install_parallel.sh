#!/bin/sh

wget 'http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2'
tar -xf parallel-latest.tar.bz2
ls
#subdir=$(tar --list -f parallel-latest.tar.bz2 | grep --max-count=1 -o 'parallel-[0-9]*/')
subdir=$(ls -1 parallel-* | grep --max-count=1 -o 'parallel-[0-9]\+')
echo "${subdir}"
cd "${subdir}"
./configure
make
make install
cd ..
rm --recursive "${subdir}" parallel-latest.tar.bz2
