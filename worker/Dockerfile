FROM debian:10.9

WORKDIR /usr/src

RUN apt-get update && apt-get upgrade --yes && apt-get install --yes zsh tmux python3 python3-pip wget openssl neovim build-essential

ADD requirements.txt /usr/src/
#ADD requirements-dev.txt /usr/src/

RUN python3 -m pip --no-cache-dir install -U pip && python3 -m pip --no-cache-dir install -r requirements.txt

ADD . /usr/src/
RUN ./install_pkgs.sh

RUN wget 'https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz' && tar -xzf gotty_linux_amd64.tar.gz && mv gotty /sbin && rm gotty_linux_amd64.tar.gz
RUN ./create_certificate.sh .

RUN apt-get install --yes less

#CMD rqworker
