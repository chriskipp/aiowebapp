#!/bin/sh

[ -d "${HOME}/dl" ] || mkdir "${HOME}/dl"
cd "${HOME}/dl"

git clone "https://github.com/zsh-users/zsh"

(
  cd zsh && \
  autoconf && \
  ( ./configure || : ) && \
  ( make || : ) && \
  sudo make install
)

rm --force --recursive zsh
cd -

# Make symlink
[ -e /bin/zsh ] || sudo ln -s $(which zsh) /bin/zsh

# Copy configuration files
cp ./conf/.zshrc "${HOME}/"
cp ./conf/.zshenv "${HOME}/"

# Change my login shell
#sudo chsh -s /bin/zsh
sudo sed -i "/${USER}/s/bash/zsh/" /etc/passwd


#  Install zsh-syntax-highlighting
[ -d "${HOME}/.zsh" ] || mkdir "${HOME}/.zsh"

(
  cd "${HOME}/.zsh"
    [ -d zsh-syntax-highlighting ] && rm --force --recursive zsh-syntax-highlighting
    git clone 'https://github.com/zsh-users/zsh-syntax-highlighting.git'
)

# Install shellhistory
python3 -m pip install -U shellhistory

