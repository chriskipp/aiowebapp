#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

PKG_LIBEVENT=$(apt-cache search libevent | grep --max-count=1 -o 'libevent[^ ]*')
sudo apt-get install libncurses-dev "${PKG_LIBEVENT}" libevent-dev byacc

git clone https://github.com/tmux/tmux.git

(
  cd tmux
  sh autogen.sh && \
	./configure && \
	make && \
	sudo make install
)

rm -fr tmux
cd -

# Copying configuration
cp conf/.tmux.conf "${HOME}"
