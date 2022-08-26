#!/bin/sh

DBFILE="data/index.sqlite"
REDISURL="redis://redis:6379"
REDIS_QUEUE="insert_textindex_queue"

cat initdb.sql | sqlite3 "${DBFILE}"

while true; do
  echo BLPOP "${REDIS_QUEUE}" 0 | redis-cli --raw -u "${REDISURL}" | sed -e '1d' -e 's/\\n/\n/g'| sqlite3 "${DBFILE}"
  echo LLEN "${REDIS_QUEUE}" | redis-cli -u "${REDISURL}"
done
