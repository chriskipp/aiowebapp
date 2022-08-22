--==========================================================
-- Create Extensions
--==========================================================

\c crawler postgres

-- run as superuser:

-- uri
CREATE EXTENSION uri;

-- pg_similarity
CREATE EXTENSION pg_similarity;

-- hypopg
CREATE EXTENSION hypopg;

-- http
CREATE EXTENSION http;
CREATE EXTENSION postgis;
--CREATE EXTENSION pgRouting;
--CREATE EXTENSION postgis_topology;
CREATE EXTENSION fuzzystrmatch;
--CREATE EXTENSION postgis_tiger_geocoder;
--ALTER EXTENSION postgis UPDATE;
--ALTER EXTENSION postgis_tiger_geocoder UPDATE;

--CREATE LANGUAGE plpython3u;

-- bloom
CREATE EXTENSION bloom;

-- pg_stat_statements
CREATE EXTENSION pg_stat_statements;
