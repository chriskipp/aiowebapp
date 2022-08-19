#!/bin/sh

#echo "shared_preload_libraries = 'pg_cron'" >> /etc/postgres/postgresql.conf
#echo "cron.database_name = 'crawler'" >> /etc/postgres/postgresql.conf

pg_ctl restart

echo "
CREATE EXTENSION pg_cron;
GRANT USAGE ON SCHEMA cron TO crawler;
" | psql --dbname=crawler

