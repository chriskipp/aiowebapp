#===========================
# postgres:15.3-alpine3.18
#===========================
FROM postgres:15.3-alpine3.18

ENV PG_VERSION=15
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD="groEMUeKaaFUJpZxoJnC"
ENV POSTGRESQL_DATABASE=postgres
ENV POSTGRES_INITDB_ARGS="--auth-local=scram-sha-256 --auth-host=scram-sha-256"
ENV PGDATA=/var/lib/postgresql/data/pgdata
ENV PGCONFIG=/etc/postgres/postgresql.conf

ENV POSTGIS_VERSION 3.3.4


# Install various extensions such as pguri, pg_similarity,
# pg_cron, hypopg, psql-http...
# All extensions are build from source files
RUN apk add --upgrade --virtual=buildutils \
    autoconf \
    automake \
    bison \
    cmake \
    clang15 \
    curl \
    curl-dev \
    ca-certificates \
    flex \
    git \
    g++ \
    libtool \
    make \
    perl-dev \
    llvm15 \
    postgresql${PG_VERSION}-dev \
    # build dependencies for postgis
    gdal-dev \
    geos-dev \
    proj-dev \
    proj-util \
    sfcgal-dev \
    cunit-dev \
    gettext-dev \
    json-c-dev \
    libxml2-dev \
    pcre2-dev \
    perl \
    protobuf-c-dev \
#
  && printf '%s\n' "Installing postgis" \
  && curl -L "https://github.com/postgis/postgis/archive/${POSTGIS_VERSION}.tar.gz" | tar -xzf - \
  && cd "postgis-${POSTGIS_VERSION}" \
  && gettextize \
  && ./autogen.sh \
  && ./configure --enable-lto \
  && make -j$(nproc) \
  && make install \
  && apk add --no-cache --virtual=postgis-rundeps \
    gdal \
    geos \
    proj \
    sfcgal \
    json-c \
    libstdc++ \
    pcre2 \
    protobuf-c \
    ca-certificates \
  && cd - \
  && rm -rf "postgis-${POSTGIS_VERSION}" \
#
  && printf '%s\n' "Installing plprofiler" \
  && git clone https://github.com/bigsql/plprofiler \
  && cd plprofiler && USE_PGXS=1 make install \
  && cd - && rm -rf plprofiler \
#
  && printf '%s\n' "Installing uriparser" \
  && curl -L 'https://github.com/uriparser/uriparser/releases/download/uriparser-0.9.7/uriparser-0.9.7.tar.gz' | tar -xzf - \
  && mkdir uriparser-0.9.7/build && cd uriparser-0.9.7/build  \
  && cmake -DCMAKE_BUILD_TYPE=Release -DURIPARSER_BUILD_DOCS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DURIPARSER_BUILD_TESTS=OFF .. \
  && make && make install && cd - && rm -rf uriparser-0.9.7 \
#
  && printf '%s\n' "Installing pguri" \
  && git clone "https://github.com/lacanoid/pguri" && cd pguri \
  && make && make install && cd - && rm -rf pguri \
  && printf '%s\n' "Installing pg_similaryti" \
  && git clone https://github.com/eulerto/pg_similarity.git  \
  && cd pg_similarity && make && make install \
  && cd - && rm -rf pg_similarity \
#
  && printf '%s\n' "Installing pg_hypopg" \
  && git clone https://github.com/HypoPG/hypopg  \
  && cd hypopg && make && make install \
  && cd - && rm -rf hypopg \
#
  && printf '%s\n' "Installing pg_cron" \
  && git clone https://github.com/citusdata/pg_cron.git \
  && cd pg_cron && make && make install \
  && cd - && rm -rf pg_cron \
#
  && printf '%s\n' "Installing pgsql-http" \
  && apk add libcurl \
  && git clone https://github.com/pramsey/pgsql-http \
  && cd pgsql-http && make && make install \
  && cd - && rm -rf pgsql-http \
#
  #&& printf '%s\n' "Installing contrib" \
  #&& git clone https://github.com/postgres/postgres \
  #&& cd postgres \
  #&& ./configure --without-readline --without-zlib \
  # --with-ssl=openssl.
  #&& cd contrib \
  #&& make all && make install \
  #&& cd - && rm -rf postgres \
#
  && printf '%s\n' "Installing bloom" \
  && git clone https://github.com/postgres/postgres \
  && cd postgres \
  && ./configure --without-readline --without-zlib \
  && cd contrib/bloom \
  && make all && make install \
  && cd - && rm -rf postgres \
#
  && printf '%s\n' "Installing libpostal" \
  && git clone https://github.com/openvenues/libpostal \
  && cd libpostal \
  && ./bootstrap.sh && ./configure \
  && ( make || make || : ) && make install \
  && cd - && rm -rf libpostal \
#
  && printf '%s\n' "Installing pgsql-postal" \
  && git clone https://github.com/pramsey/pgsql-postal \
  && cd pgsql-postal \
  && make && make install \
  && cd - && rm -rf pgsql-postal \
#
  && printf '%s\n' "Removing build dependencies" \
  && apk del --purge buildutils \
  && rm -rf /root/.cache /tmp/*

COPY ./initdb /docker-entrypoint-initdb.d
COPY ./conf/postgresql.conf /etc/postgres/postgresql.conf
COPY ./conf/pg_hba.conf /etc/postgres/pg_hba.conf

