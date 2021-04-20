#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
        sudo apt-get upgrade --yes && \
        sudo apt-get install --yes curl


# Get the source code e.g.
# git clone https://github.com/tmux/tmux.git
# wget 'https://nodejs.org/latest'
latest_url="https://nodejs.org/dist/latest/"
dist_url=$(curl  "${latest_url}" | grep -o "node[^>]*linux-x64.tar.xz" | head -n1)
echo "Downloading ${latest_url}${dist_url}..."
wget "${latest_url}${dist_url}"


# Evtl. unpack archives
tar -xf "${dist_url}"

# Configure, build and install the Package
(
  cd $(basename --suffix=".tar.xz"  "${dist_url}") && \
  sudo cp --recursive "bin" "include" "lib" "share" /"usr"
)

# Remove Source Files
rm --force --recursive node-*-linux-x64*
cd -
