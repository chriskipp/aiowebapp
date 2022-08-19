#===========================
# postgres:14.4-alpine3.16
#===========================
FROM postgres:14.5-alpine3.16

ENV PG_VERSION=14
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD="groEMUeKaaFUJpZxoJnC"
ENV POSTGRESQL_DATABASE=crawler
ENV POSTGRES_INITDB_ARGS="--auth-local=scram-sha-256 --auth-host=scram-sha-256"
ENV PGDATA=/var/lib/postgresql/data/pgdata
ENV PGCONFIG=/etc/postgres/postgresql.conf

COPY ./conf/postgresql.conf /etc/postgres/postgresql.conf
COPY ./initdb /docker-entrypoint-initdb.d
COPY ssl/* /var/lib/postgresql/
RUN chown 0:70 /var/lib/postgresql/server.key

# Install pguri, pg_similarity, pg_cron, hypopg, psql-http
RUN apk add make postgresql14-dev curl ca-certificates cmake g++ git curl-dev perl-dev flex bison \
  && curl -L 'https://github.com/uriparser/uriparser/releases/download/uriparser-0.9.6/uriparser-0.9.6.tar.gz' \
  | tar -xzf - && mkdir uriparser-0.9.6/build && cd uriparser-0.9.6/build \
  && cmake -DCMAKE_BUILD_TYPE=Release -DURIPARSER_BUILD_DOCS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DURIPARSER_BUILD_TESTS=OFF .. \
  && make && make install && cd - && rm -rf uriparser-0.9.6 \
  && git clone https://github.com/petere/pguri && cd pguri \
  && make && make install && cd - && rm -rf pguri \
  && git clone https://github.com/eulerto/pg_similarity.git  \
  && cd pg_similarity && make && make install \
  && cd - && rm -rf pg_similarity \
  && git clone https://github.com/HypoPG/hypopg  \
  && cd hypopg && make && make install \
  && cd - && rm -rf hypopg \
  && git clone https://github.com/citusdata/pg_cron.git \
  && cd pg_cron && make && make install \
  && cd - && rm -rf pg_cron \
  && apk add libcurl \
  && git clone https://github.com/pramsey/pgsql-http \
  && cd pgsql-http && make && make install \
  && cd - && rm -rf pgsql-http

RUN printf '%s\n' "Installing bloom" \
    && git clone https://github.com/postgres/postgres \
    && cd postgres \
    && ./configure --without-readline --without-zlib \
    && cd contrib/bloom \
    && make all \
    && make install \
    && cd - \
    && rm -rf postgres \
    && printf '%s\n' "Removing build dependencies" \
    && apk del make postgresql14-dev curl ca-certificates cmake g++ git curl-dev perl-dev flex bison \
    && apk add postgis

EXPOSE 5432

#CMD postgres \
#  -c config_file=/etc/postgres/postgresql.conf
#  -c ssl=on \
#  -c ssl_cert_file=/var/lib/postgresql/server.crt \
#  -c ssl_key_file=/var/lib/postgresql/server.key \

