#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Get the source code e.g.
git clone https://github.com/ytdl-org/youtube-dl.git

# Configure, build and install the Package
(
  cd youtube-dl
  sudo python3 setup.py install
)

# Remove Source Files
sudo rm --force --recursive youtube-dl
cd -
