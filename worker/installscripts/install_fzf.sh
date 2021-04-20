#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Get the source code
releases_url='https://github.com/junegunn/fzf/releases'
latest_realease_url=$(curl -s "${releases_url}" | grep --max-count=1 -o '"[^"]*fzf-[0-9.]*-linux_amd64.tar.gz"' | tr -d '"')
source_archive=$(basename "${latest_realease_url}")
wget -O "${source_archive}" "https://github.com/${latest_realease_url}"

# Evtl. unpack archives
tar -xf "${source_archive}"

# Install fzf
sudo mv fzf /sbin/


# Remove Source Files
rm --force --recursive "${source_archive}"
cd -

# Install fzf-tmux
[ -d "${HOME}/bin" ] || mkdir "${HOME}/bin"
cp ../bin/fzf-tmux "${HOME}/bin"
echo "${source_archive}"
