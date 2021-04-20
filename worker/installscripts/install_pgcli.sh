#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Update repositories and install build dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes postgresql-server-dev-all libpq-dev

# Get the source code e.g.
git clone https://github.com/psycopg/psycopg2

# Configure, build and install the Package
(
  cd psycopg2
  python3 setup.py build_ext --pg-config ~/init/bin/pg_config install --user
  sudo python3 setup.py build_ext --pg-config ~/init/bin/pg_config install
)

# Remove Source Files
rm --force --recursive psycopg2
cd -


sudo apt-get purge --yes postgresql-server-dev-all && \
	sudo apt-get --yes autoremove && \
	sudo apt-get autoclean
