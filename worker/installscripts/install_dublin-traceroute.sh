#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes libpcap-dev libjsoncpp-dev libtins-dev libdublintraceroute-dev libtins-dev libdublintraceroute-dev libdublintraceroute0 graphviz graphviz-dev

# Get the source code e.g.
git clone https://github.com/insomniacslk/python-dublin-traceroute.git

# Configure, build and install the Package
(
  cd python-dublin-traceroute
  pip3 install -r requirements.txt --user
  python setup.py install --user
)

# If compilation fails anyway:
pip3 install dublintraceroute --user
pip3 install pygraphviz --user


# Remove Source Files
rm --force --recursive "python-dublin-traceroute"
cd -
