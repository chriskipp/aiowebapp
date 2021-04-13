      CREATE DATABASE crawling;

DO
$do2$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'crawling') THEN

      CREATE ROLE crawling LOGIN PASSWORD 'crawl';
      GRANT ALL PRIVILEGES ON DATABASE crawling TO crawling;
   END IF;
END
$do2$;

ALTER DATABASE crawling OWNER TO crawling;

\c crawling

CREATE TABLE IF NOT EXISTS domains (
   id 	  INTEGER PRIMARY KEY,
   domain VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS path (
   id 	  INTEGER PRIMARY KEY,
   path VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS url (
   id 	  INTEGER PRIMARY KEY,
   domain_id INTEGER,
   path_id INTEGER,
   CONSTRAINT fk_domain
      FOREIGN KEY(domain_id) 
	  REFERENCES domains(id),
   CONSTRAINT fk_path
      FOREIGN KEY(path_id) 
	  REFERENCES path(id)
);

