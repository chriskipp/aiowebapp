--==========================================================
-- Database
--==========================================================

\c crawler postgres

CREATE SCHEMA urls;
ALTER SCHEMA urls OWNER TO crawler;
GRANT ALL PRIVILEGES ON SCHEMA urls TO crawler;

--==========================================================
-- Extentions
--==========================================================

\c crawler postgres

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
-- Create Table www
--==========================================================
CREATE TABLE IF NOT EXISTS urls.www
(
    id                 SMALLSERIAL PRIMARY KEY,
    www                VARCHAR(4) UNIQUE NOT NULL
);

--==========================================================
-- Create Table scheme
--==========================================================
CREATE TABLE IF NOT EXISTS urls.scheme
(
    id                 SMALLSERIAL PRIMARY KEY,
    scheme             VARCHAR(16) UNIQUE NOT NULL
);

--==========================================================
-- Create Table domains
--==========================================================
CREATE TABLE IF NOT EXISTS urls.domains
(
    id                 SERIAL PRIMARY KEY,
    scheme_id          SMALLINT NOT NULL REFERENCES
                           urls.scheme ON DELETE RESTRICT,
    www_id             SMALLINT NOT NULL REFERENCES
                           urls.www ON DELETE RESTRICT,
    domain             VARCHAR NOT NULL,
    insert_date        TIMESTAMP WITH TIME ZONE,
    change_date        TIMESTAMP WITH TIME ZONE,
                       UNIQUE(www_id, domain)
);

CREATE TRIGGER t_set_inserted_date_domains
    BEFORE INSERT ON urls.domains
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_domains
    BEFORE INSERT ON urls.domains
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

CREATE INDEX
    CONCURRENTLY
    ON urls.domains (domain);

CREATE UNIQUE INDEX
    CONCURRENTLY
    ON urls.domains (www_id, domain);

--==========================================================
-- Create Table paths
--==========================================================
CREATE TABLE IF NOT EXISTS urls.paths
(
    id 			SERIAL PRIMARY KEY,
    path 		VARCHAR UNIQUE NOT NULL,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER t_set_insert_date_paths
    BEFORE INSERT ON urls.paths
    FOR EACH ROW
EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_paths
    BEFORE INSERT ON urls.paths
    FOR EACH ROW
EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
    CONCURRENTLY
    ON urls.paths (path);


--==========================================================
-- Create Table endpoints
--==========================================================
CREATE TABLE IF NOT EXISTS urls.endpoints
(
    id 			SERIAL PRIMARY KEY,
    domain_id    	INTEGER NOT NULL REFERENCES
        	            urls.domains ON DELETE RESTRICT,
    path_id      	INTEGER NOT NULL REFERENCES
        	            urls.paths ON DELETE RESTRICT,
    		        UNIQUE (domain_id, path_id)
);

CREATE UNIQUE INDEX
    CONCURRENTLY
    ON urls.endpoints (domain_id, path_id);


--==========================================================
-- Create Table endpoints_collect
--==========================================================
CREATE TABLE IF NOT EXISTS urls.endpoints_collect
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
    BEFORE INSERT ON urls.endpoints_collect
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_endpoints_collect
    BEFORE INSERT ON urls.endpoints_collect
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table domain_info
--==========================================================
CREATE TABLE IF NOT EXISTS urls.domain_info (
    domain_id 		INTEGER UNIQUE NOT NULL REFERENCES
                            urls.domains ON DELETE RESTRICT,
    toplevel 		VARCHAR(16),
    name 		VARCHAR,
    description 	TEXT,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE
 );

CREATE TRIGGER t_set_insert_date_domain_info
    BEFORE INSERT ON urls.domain_info
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_domain_info
    BEFORE INSERT ON urls.domain_info
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table query_parts
--==========================================================
CREATE TABLE IF NOT EXISTS urls.query_parts (
    id                  SERIAL PRIMARY KEY,
    key                 VARCHAR,
    value               VARCHAR,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE,
                        UNIQUE(key, value)
);

CREATE TRIGGER t_set_insert_date_query_parts
    BEFORE INSERT ON urls.query_parts
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_query_parts
    BEFORE INSERT ON urls.query_parts
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
    CONCURRENTLY
    ON urls.query_parts (key, value);

--==========================================================
-- Create Table queries
--==========================================================
CREATE TABLE IF NOT EXISTS urls.queries (
    id                  SERIAL PRIMARY KEY,
    query_part_ids      INTEGER[] UNIQUE,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER t_set_insert_date_queries
    BEFORE INSERT ON urls.queries
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_queries
    BEFORE INSERT ON urls.queries
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
    CONCURRENTLY
    ON urls.queries(query_part_ids);


--==========================================================
-- Create Table urls
--==========================================================
CREATE TABLE IF NOT EXISTS urls.urls (
    fingerprint         UUID PRIMARY KEY,
    endpoint_id         INTEGER REFERENCES
                            urls.endpoints ON DELETE RESTRICT,
    query_id            INTEGER REFERENCES
                            urls.queries ON DELETE RESTRICT,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE,
                        UNIQUE(endpoint_id, query_id)
);

CREATE TRIGGER t_set_insert_date_urls
    BEFORE INSERT ON urls.urls
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_urls
    BEFORE INSERT ON urls.urls
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

CREATE UNIQUE INDEX
    CONCURRENTLY
    ON urls.urls(fingerprint);


--==========================================================
-- Create Table url_info
--==========================================================
CREATE TABLE IF NOT EXISTS urls.url_info (
   fingerprint 		UUID NOT NULL REFERENCES
                            urls.urls ON DELETE RESTRICT,
   response_status 	SMALLINT,
   mimetype 		VARCHAR(64),
   language 		VARCHAR(5),
   size 		INTEGER,
   title 		TEXT,
   insert_date 		TIMESTAMP WITH TIME ZONE,
   change_date 		TIMESTAMP WITH TIME ZONE
);

CREATE INDEX
    CONCURRENTLY
    ON urls.url_info(fingerprint);

CREATE TRIGGER t_set_insert_date_url_info
    BEFORE INSERT ON urls.url_info
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_url_info
    BEFORE INSERT ON urls.url_info
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table urls_collect
--==========================================================
CREATE TABLE IF NOT EXISTS urls.urls_collect (
    fingerprint         UUID NOT NULL,
    scheme              VARCHAR(16),
    www                 VARCHAR(4),
    domain              VARCHAR,
    path                VARCHAR,
    query               VARCHAR,
    insert_date         TIMESTAMP WITH TIME ZONE,
    change_date         TIMESTAMP WITH TIME ZONE
);


CREATE TRIGGER t_set_insert_date_urls_collect
    BEFORE INSERT ON urls.urls_collect
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_queries_collect
    BEFORE INSERT ON urls.urls_collect
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();

--==========================================================
-- Create Table links
--==========================================================
CREATE TABLE IF NOT EXISTS urls.links (
    id                  BIGSERIAL PRIMARY KEY,
    source              UUID NOT NULL REFERENCES
		            urls.urls ON DELETE RESTRICT,
    dest                UUID NOT NULL REFERENCES
                            urls.urls ON DELETE RESTRICT
);

--==========================================================
-- Create Table link_info
--==========================================================
CREATE TABLE IF NOT EXISTS urls.link_info (
    id                  BIGSERIAL PRIMARY KEY,
    linktext            VARCHAR,
    insert_date 	TIMESTAMP WITH TIME ZONE,
    change_date 	TIMESTAMP WITH TIME ZONE
);

CREATE TRIGGER t_set_insert_date_link_info
    BEFORE INSERT ON urls.link_info
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_insert_date();

CREATE TRIGGER t_set_change_date_link_info
    BEFORE INSERT ON urls.link_info
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_change_date();


--==========================================================
-- Create Views
--==========================================================
CREATE OR REPLACE VIEW urls.v_endpoints AS
SELECT
    e.id AS endpunkt_id,
    d.id AS domain_id,
    p.id AS path_id,
    s.scheme AS scheme,
    w.www AS www,
    d.domain AS domain,
    p.path AS path,
    s.scheme || '://'
        || w.www || d.domain 
	|| p.path
        AS endpoint_url
FROM urls.endpoints e
INNER JOIN urls.domains d
    ON d.id = e.domain_id
INNER JOIN urls.paths p
    ON p.id = e.path_id
INNER JOIN urls.scheme s
    ON d.scheme_id = s.id
INNER JOIN urls.www w
    ON d.www_id = w.id
;

----==========================================================
---- Create Function to insert urls
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

--CREATE OR REPLACE FUNCTION f_insert_query_part(
--    k VARCHAR,
--    v VARCHAR)
--RETURNS INTEGER
--LANGUAGE SQL
--AS $$
--    WITH i AS (
--        INSERT INTO query_parts (
--            key, value
--        ) SELECT k, v
--        WHERE NOT EXISTS (
--            SELECT 1
--        FROM query_parts qp
--        WHERE qp.key = k
--            AND qp.value = v
--        ) RETURNING id
--    )
--     SELECT id FROM i
--    UNION
--    SELECT id
--    FROM query_parts qp
--    WHERE qp.key = k
--         AND qp.value = v;
--$$;

CREATE OR REPLACE FUNCTION urls.f_insert_path(
    p VARCHAR
) RETURNS INTEGER
LANGUAGE SQL
AS $$
    WITH i AS (
        INSERT INTO urls.paths (
            path
        ) SELECT p
        WHERE NOT EXISTS (
            SELECT 1
            FROM urls.paths ps
            WHERE ps.path = p
        ) RETURNING id
    )
    SELECT id FROM i
    UNION
    SELECT id FROM urls.paths ps
    WHERE ps.path = p;
$$;

CREATE OR REPLACE FUNCTION urls.f_insert_domain(
    _scheme VARCHAR,
    _www VARCHAR,
    _domain VARCHAR
) RETURNS INTEGER
AS $$
    DECLARE wwwid INTEGER;
    DECLARE schemeid INTEGER;
    DECLARE nid INTEGER;
    BEGIN
        SELECT id
        INTO wwwid
        FROM urls.www AS w
        WHERE w.www = _www;
    
        SELECT id
        INTO schemeid
        FROM urls.scheme AS s
        WHERE s.scheme = _scheme;
    
        WITH i AS (
            INSERT INTO urls.domains (
                scheme_id, www_id, domain
            )
            SELECT schemeid, wwwid, _domain
            WHERE NOT EXISTS (
                SELECT 1
                FROM urls.domains d
                WHERE d.domain = _domain
                    AND d.www_id = wwwid
            )
            RETURNING id
        )
        SELECT id
	INTO nid
	FROM i
        UNION
        SELECT id
	FROM urls.domains d
        WHERE d.domain = _domain
            AND d.www_id = wwwid
        ;
	RETURN nid;
    END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION urls.f_insert_query_parts(
    querystring VARCHAR
) RETURNS INTEGER[]
LANGUAGE SQL
AS $$
    WITH q AS (
        SELECT UNNEST(
	    STRING_TO_ARRAY(
		querystring, '&'
	    )) AS q
    ), kv AS (
        SELECT (
            STRING_TO_ARRAY(q, '=')
        )[1] AS k,
            ARRAY_TO_STRING((
	        STRING_TO_ARRAY(q, '=')
            )[2:], '=') AS v
        FROM q
	ORDER BY k, v
    ), i AS (
        INSERT INTO urls.query_parts (
            key, value
        ) SELECT
	  DISTINCT
            k, v
          FROM kv
          WHERE NOT EXISTS (
          SELECT 1
              FROM urls.query_parts qp
              WHERE kv.k = qp.key
                  AND kv.v = qp.value
         ) RETURNING id
    ), res AS (
        SELECT id FROM i
        UNION
        SELECT id
        FROM urls.query_parts qp
        WHERE EXISTS (
            SELECT 1
            FROM kv
            WHERE qp.key = kv.k
                AND qp.value = kv.v)
    )
    SELECT ARRAY_AGG(id)
    FROM res
$$;


CREATE OR REPLACE FUNCTION urls.f_insert_query(
    query_parts INTEGER[]
) RETURNS INTEGER
LANGUAGE SQL
AS $$
    WITH parr as (
        SELECT query_parts v
	WHERE query_parts IS NOT NULL
    ), qid AS (
        INSERT INTO urls.queries (query_part_ids)
        SELECT v FROM parr
        WHERE NOT EXISTS (
            SELECT 1
            FROM urls.queries q
            WHERE q.query_part_ids =  parr.v
        )
        RETURNING id
    )
    SELECT id
    FROM qid
    UNION
    SELECT id
    FROM urls.queries q
    INNER JOIN parr
        ON q.query_part_ids = parr.v
$$;


CREATE OR REPLACE FUNCTION urls.f_insert_endpoint(
    _scheme VARCHAR,
    _www VARCHAR,
    _domain VARCHAR,
    _path VARCHAR
) RETURNS INTEGER
LANGUAGE SQL
AS $$
    WITH ne AS (
        SELECT
            urls.f_insert_domain(
                _scheme,
                _www,
                _domain
            ) AS _domain_id,
            urls.f_insert_path(
                _path
            ) AS _path_id
        ), ie AS (
           INSERT INTO urls.endpoints (
               domain_id, path_id
           )
           SELECT
               _domain_id,
               _path_id
           FROM ne
           WHERE NOT EXISTS (
               SELECT 1
               FROM urls.endpoints e
                   WHERE e.domain_id = ne._domain_id
                       AND e.path_id = ne._path_id
           ) RETURNING id
        )
    SELECT id
    FROM ie
    UNION
    SELECT id
    FROM urls.endpoints e
    WHERE EXISTS (
        SELECT 1
        FROM ne
            WHERE e.domain_id = ne._domain_id
                AND e.path_id = ne._path_id
    );
$$;

CREATE OR REPLACE FUNCTION urls.f_insert_url(
    _fingerprint VARCHAR,
    _scheme VARCHAR,
    _www VARCHAR,
    _domain VARCHAR,
    _path VARCHAR DEFAULT NULL,
    _query VARCHAR DEFAULT NULL
) RETURNS UUID
LANGUAGE SQL
AS $$
    WITH eqi AS (
        SELECT urls.f_insert_endpoint(
         _scheme,
         _www,
         _domain,
         _path
        ) AS eid ,
        urls.f_insert_query(
            urls.f_insert_query_parts(
               _query
            )
        ) qid
    ), i AS (
        INSERT INTO urls.urls (
            fingerprint, endpoint_id, query_id
        )
        SELECT _fingerprint::UUID, eid, qid
        FROM eqi
        WHERE NOT EXISTS (
            SELECT 1
            FROM urls.urls u
            WHERE u.fingerprint = _fingerprint::UUID
        ) RETURNING fingerprint
    )
    SELECT fingerprint
    FROM i
    UNION
SELECT u.fingerprint
    FROM urls.urls u
    WHERE u.fingerprint = _fingerprint::UUID
    ;
$$;

CREATE OR REPLACE FUNCTION urls.f_build_query_string(
    querypartids INTEGER[]
)
RETURNS VARCHAR
LANGUAGE SQL
AS $$
    SELECT
        ARRAY_TO_STRING(ARRAY_AGG(
	    key || '=' || value
        ), '&')
    FROM urls.query_parts
    WHERE id = ANY(querypartids);
$$;

--==========================================================
-- Create View v_urls
--==========================================================
CREATE OR REPLACE VIEW urls.v_urls AS
SELECT
    u.fingerprint AS fingerprint,
    e.id AS endpunkt_id,
    d.id AS domain_id,
    p.id AS path_id,
    q.id AS query_id,
    q.query_part_ids AS query_parts,
    s.scheme AS scheme,
    w.www AS www,
    d.domain AS domain,
    p.path AS path,
    urls.f_build_query_string(q.query_part_ids) AS query_string,
    s.scheme || '://'
        || w.www || d.domain
        || p.path
        AS endpoint_url,
    CASE
        WHEN urls.f_build_query_string(q.query_part_ids) IS NULL THEN
            s.scheme || '://'
                || w.www || d.domain
                || p.path
        ELSE
            s.scheme || '://'
                || w.www || d.domain
                || p.path || '?'
                || urls.f_build_query_string(q.query_part_ids)
    END AS url

FROM urls.urls u
INNER JOIN urls.endpoints e
    ON e.id = u.endpoint_id
INNER JOIN urls.domains d
    ON d.id = e.domain_id
INNER JOIN urls.scheme s
    ON d.scheme_id = s.id
INNER JOIN urls.www w
    ON d.www_id = w.id
INNER JOIN urls.paths p
    ON p.id = e.path_id
LEFT JOIN urls.queries q
    ON q.id = u.query_id
;


CREATE OR REPLACE FUNCTION urls.f_build_url(
    fingerprint UUID
)
RETURNS VARCHAR
LANGUAGE SQL
AS $$
    SELECT
        CASE
            WHEN urls.f_build_query_string(q.query_part_ids) IS NULL THEN
                s.scheme || '://'
                    || w.www || d.domain
                    || p.path
            ELSE
                s.scheme || '://'
                    || w.www || d.domain
                    || p.path || '?'
                    || urls.f_build_query_string(q.query_part_ids)
        END AS url
        FROM urls.urls u
        INNER JOIN urls.endpoints e
            ON e.id = u.endpoint_id
        INNER JOIN urls.domains d
            ON d.id = e.domain_id
        INNER JOIN urls.scheme s
            ON s.id = d.scheme_id
        INNER JOIN urls.www w
            ON w.id = d.www_id
        INNER JOIN urls.paths p
            ON p.id = e.path_id
        LEFT JOIN urls.queries q
            ON u.query_id = q.id;
$$;

CREATE OR REPLACE FUNCTION urls.calc_fingerprint(_url TEXT)
  RETURNS UUID
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN MD5('GET' || _url)::UUID;
END; $$;


ALTER TABLE urls.domains OWNER TO crawler;
ALTER TABLE urls.domain_info OWNER TO crawler;
ALTER TABLE urls.paths OWNER TO crawler;
ALTER TABLE urls.endpoints OWNER TO crawler;
ALTER TABLE urls.endpoints_collect OWNER TO crawler;
ALTER TABLE urls.url_info OWNER TO crawler;
ALTER TABLE urls.links OWNER TO crawler;
ALTER TABLE urls.link_info OWNER TO crawler;
ALTER TABLE urls.scheme OWNER TO crawler;
GRANT ALL PRIVILEGES ON urls.scheme TO crawler;
ALTER TABLE urls.www OWNER TO crawler;
GRANT ALL PRIVILEGES ON urls.www TO crawler;
ALTER TABLE urls.query_parts OWNER TO crawler;
ALTER TABLE urls.queries OWNER TO crawler;
ALTER TABLE urls.urls OWNER TO crawler;
ALTER TABLE urls.urls_collect OWNER TO crawler;

ALTER VIEW urls.v_endpoints OWNER TO crawler;
ALTER VIEW urls.v_urls OWNER TO crawler;

ALTER FUNCTION urls.f_insert_url OWNER TO crawler;
ALTER FUNCTION urls.f_insert_domain OWNER TO crawler;
ALTER FUNCTION urls.f_insert_endpoint OWNER TO crawler;
ALTER FUNCTION urls.f_insert_path OWNER TO crawler;
ALTER FUNCTION urls.f_insert_query OWNER TO crawler;
ALTER FUNCTION urls.f_insert_query_parts OWNER TO crawler;
ALTER FUNCTION urls.f_build_query_string OWNER TO crawler;
ALTER FUNCTION urls.f_build_url OWNER TO crawler;

CREATE OR REPLACE FUNCTION urls.f_insert_url_collect(
   fingerprint VARCHAR,
   scheme VARCHAR,
   www VARCHAR,
   domain VARCHAR,
   path VARCHAR DEFAULT NULL,
   query VARCHAR DEFAULT NULL
 ) RETURNS void
 LANGUAGE SQL
 AS $$
 INSERT INTO urls.urls_collect(
   fingerprint, scheme, www, domain, path, query
 ) VALUES (
   fingerprint::UUID, scheme, www, domain, path, query
 );
 $$;




--==========================================================
-- Inserts common URL schemes
--==========================================================
INSERT INTO urls.scheme (scheme) VALUES ('https');
INSERT INTO urls.scheme (scheme) VALUES ('http');
INSERT INTO urls.scheme (scheme) VALUES ('socks4');
INSERT INTO urls.scheme (scheme) VALUES ('socks5');

--==========================================================
-- Inserts 'www.' and '' (empty string) domain prefix
--==========================================================
INSERT INTO urls.www (www) VALUES ('');
INSERT INTO urls.www (www) VALUES ('www.');


--==========================================================
-- Tags
--==========================================================
CREATE TABLE IF NOT EXISTS urls.tags (
  id SERIAL PRIMARY KEY,
  parent_id INTEGER,
  label VARCHAR(127),
  value VARCHAR(127),
  type VARCHAR(63)
);

CREATE TABLE IF NOT EXISTS urls.url_tags (
  fingerprint UUID
    REFERENCES urls.urls(fingerprint),
  tag_id INTEGER
    REFERENCES urls.tags(id)
);

CREATE TABLE IF NOT EXISTS urls.emails (
    fingerprint UUID
      REFERENCES urls.urls(fingerprint),
    email VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS urls.phones (
    fingerprint UUID
    REFERENCES urls.urls(fingerprint),
    phone VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS urls.socnets (
    fingerprint UUID
      REFERENCES urls.urls(fingerprint),
    socnet VARCHAR(32) NOT NULL,
    socnetlink UUID
      REFERENCES urls.urls(fingerprint)
);

CREATE TABLE IF NOT EXISTS urls.addresses (
    fingerprint UUID
      REFERENCES urls.urls(fingerprint),
    house TEXT,
    road TEXT,
    house_number TEXT,
    postcode TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS urls.products (
    fingerprint UUID
      REFERENCES urls.urls(fingerprint),
    product VARCHAR NOT NULL
);

