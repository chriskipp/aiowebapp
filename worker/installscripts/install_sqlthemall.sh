#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

# Get the source code e.g.
git clone 'https://github.com/chriskipp/sqlthemall'

# Install the Package
(
  cd sqlthemall
  python3 setup.py install --user
)

# Remove Source Files
rm --force --recursive sqlthemall
cd -
