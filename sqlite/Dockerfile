FROM alpine:3.16.2

WORKDIR /src
COPY install_sqlite3.sh .
COPY initdb.sql .

RUN printf "http://dl-cdn.alpinelinux.org/alpine/edge/community" \
  >> /etc/apk/repositories && \
  apk add --update --no-cache --virtual=buildutils \
    musl-dev \
    zlib-dev \
    ncurses-dev \
    readline-dev \
    linux-headers \
    upx \
    make \
    gcc \
    wget \
    tcl \
    && apk add --update --no-cache \
    libgcc \
    readline \
    fakeroot \
    ccache \
    binutils \
    file \
    unzip \
    zlib-static \
    libhistory \
    readline-static \
    ncurses-static \
  && ./install_sqlite3.sh \
  && rm install_sqlite3.sh \
  && apk del buildutils

RUN cat initdb.sql | sqlite3 db.sqlite

CMD ["tail", "-F", "initdb.sql"]
