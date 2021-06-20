--==========================================================
-- Schema
--==========================================================

CREATE DATABASE weblog;
CREATE USER weblog WITH PASSWORD 'weblog';
ALTER DATABASE weblog OWNER TO weblog;
GRANT ALL PRIVILEGES ON DATABASE weblog TO weblog;


\c weblog


--==========================================================
-- Define Trigger Functions
--==========================================================

CREATE OR REPLACE FUNCTION trigger_set_insert_date()
RETURNS TRIGGER AS $$
BEGIN
  NEW.insert_date = NOW();
  NEW.change_date = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trigger_set_change_date()
RETURNS TRIGGER AS $$
BEGIN
  NEW.change_date = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--==========================================================
-- Create Table domains
--==========================================================
CREATE TABLE IF NOT EXISTS domains
(
    id SERIAL          PRIMARY KEY,
    scheme             VARCHAR(8) NOT NULL,
    domain             VARCHAR NOT NULL UNIQUE,
    www                VARCHAR(4) NOT NULL,
    insert_date        TIMESTAMP WITH TIME ZONE,
    change_date        TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER t_set_inserted_date_domains
BEFORE INSERT ON domains
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_domains
BEFORE INSERT ON domains
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
CONCURRENTLY
ON domains (domain);

--==========================================================
-- Create Table paths
--==========================================================
CREATE TABLE IF NOT EXISTS paths
(
    id 			SERIAL PRIMARY KEY,
    path 		VARCHAR UNIQUE NOT NULL,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER t_set_insert_date_paths
BEFORE INSERT ON paths
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_paths
BEFORE INSERT ON paths
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
CONCURRENTLY
ON paths (path);


--==========================================================
-- Create Table endpoints
--==========================================================
CREATE TABLE IF NOT EXISTS endpoints
(
    id 			SERIAL PRIMARY KEY,
    domain_id    	INTEGER NOT NULL REFERENCES
        	domains ON DELETE RESTRICT,
    path_id      	INTEGER NOT NULL REFERENCES
        	paths ON DELETE RESTRICT,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE,
    		UNIQUE (domain_id, path_id)
);

CREATE TRIGGER t_set_insert_date_endpoints
BEFORE INSERT ON endpoints
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_endpoints
BEFORE INSERT ON endpoints
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
CONCURRENTLY
ON endpoints (domain_id, path_id);


--==========================================================
-- Create Table endpoints_collect
--==========================================================
CREATE TABLE IF NOT EXISTS endpoints_collect
(
    _id           SERIAL PRIMARY KEY,
    scheme        VARCHAR NOT NULL,
    www           VARCHAR NOT NULL,
    domain        VARCHAR NOT NULL,
    path          VARCHAR NOT NULL,
    insert_date   TIMESTAMP WITH TIME ZONE,
    change_date   TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER t_set_insert_date_endpoints_collect
BEFORE INSERT ON endpoints_collect
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_endpoints_collect
BEFORE INSERT ON endpoints_collect
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table endpoints_info
--==========================================================
CREATE TABLE IF NOT EXISTS endpoint_info (
   endpoint_id 		INTEGER,
   response_status 	SMALLINT,
   mimetype 		VARCHAR(64),
   language 		VARCHAR(5),
   size 		INTEGER,
   title 		TEXT,
   insert_date 		TIMESTAMP WITH TIME ZONE,
   change_date 		TIMESTAMP WITH TIME ZONE
 );

CREATE TRIGGER t_set_insert_date_endpoint_info
BEFORE INSERT ON endpoint_info
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_endpoint_info
BEFORE INSERT ON endpoint_info
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table domain_info
--==========================================================
CREATE TABLE IF NOT EXISTS domain_info (
   domain_id 		INTEGER,
   toplevel 		VARCHAR(16),
   name 		VARCHAR,
   description 		TEXT,
   insert_date 		TIMESTAMP WITH TIME ZONE,
   change_date 		TIMESTAMP WITH TIME ZONE
 );

CREATE TRIGGER t_set_insert_date_domain_info
BEFORE INSERT ON domain_info
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_domain_info
BEFORE INSERT ON domain_info
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table links
--==========================================================
CREATE TABLE IF NOT EXISTS links (
  source BIGINT,
  dest BIGINT,
  count SMALLINT
);

--==========================================================
-- Create Table link_info
--==========================================================
CREATE TABLE IF NOT EXISTS link_info (
  id SERIAL PRIMARY KEY,
  source BIGINT,
  dest BIGINT,
  linktext VARCHAR
);

--==========================================================
-- Create Views
--==========================================================
 CREATE OR REPLACE VIEW v_endpunkte AS SELECT
   e.id AS endpunkt_id,
   d.id AS domain_id,
   p.id AS path_id,
   d.scheme AS scheme,
   d.www AS www,
   d.domain AS domain,
   p.path AS path,
   d.scheme || '://' || d.www || d.domain || p.path AS url
 FROM endpoints e
 INNER JOIN domains d
    ON d.id = e.domain_id
 INNER JOIN paths p
    ON p.id = e.path_id;


----==========================================================
---- Create Function to inseert urls
----==========================================================
-- CREATE OR REPLACE FUNCTION _insert_url(scheme VARCHAR, www VARCHAR, domain VARCHAR, path VARCHAR) RETURNS INTEGER
-- LANGUAGE sql AS
-- $$
-- WITH val AS (
--          SELECT scheme, www, domain, path
--    ), sel AS (
--      SELECT d.id AS domain_id, p.id AS path_id, v.scheme, SUBSTR(v.www, 0, 3) as www, v.domain, v.path
--      FROM val AS v
--      LEFT JOIN domains d ON v.domain = d.domain
--      LEFT JOIN paths p ON v.path = p.path
--    ),
-- _ins_d AS (
--    INSERT INTO domains (
--      scheme, www, domain
--    ) SELECT MAX(scheme), MAX(www), domain
--    FROM sel
--    WHERE sel.domain_id IS NULL
--    GROUP BY domain
--    RETURNING id, domain
--    ),
-- _ins_p AS (
--    INSERT INTO paths (
--      path
--    ) SELECT DISTINCT path
--    FROM sel
--    WHERE sel.path_id IS NULL
--    RETURNING id, path
--    ),
-- _ins_e AS (
-- INSERT INTO endpoints (
--   domain_id, path_id
-- ) SELECT DISTINCT
--   COALESCE(s.domain_id, d.id) AS domain_id,
--   COALESCE(s.path_id, p.id) AS path_id
-- FROM sel AS s
-- LEFT JOIN _ins_d d on s.domain = d.domain
-- LEFT JOIN _ins_p p on s.path = p.path
-- WHERE NOT EXISTS (SELECT 1
--   FROM endpoints e
--   WHERE e.domain_id = s.domain_id
--     AND e.path_id = s.path_id
--   )
--   RETURNING id, domain_id, path_id
-- )
-- SELECT e.id FROM sel s
-- INNER JOIN endpoints e
--  ON s.domain_id = e.domain_id
--  AND s.path_id = e.path_id
-- UNION
-- SELECT id FROM _ins_e
-- ;
-- $$;

ALTER TABLE domains OWNER TO weblog;
ALTER TABLE domain_info OWNER TO weblog;
ALTER TABLE paths OWNER TO weblog;
ALTER TABLE endpoints OWNER TO weblog;
ALTER TABLE endpoints_collect OWNER TO weblog;
ALTER TABLE endpoint_info OWNER TO weblog;
ALTER TABLE links OWNER TO weblog;
ALTER TABLE link_info OWNER TO weblog;

