\c app

-- create users table
CREATE TABLE IF NOT EXISTS users
(
  id integer NOT NULL,
  login character varying(256) NOT NULL,
  passwd character varying(256) NOT NULL,
  is_superuser boolean NOT NULL DEFAULT false,
  disabled boolean NOT NULL DEFAULT false,
  CONSTRAINT user_pkey PRIMARY KEY (id),
  CONSTRAINT user_login_key UNIQUE (login)
);

ALTER TABLE users OWNER TO app;

-- and permissions for them
CREATE TABLE IF NOT EXISTS permissions
(
  id integer NOT NULL,
  user_id integer NOT NULL,
  perm_name character varying(64) NOT NULL,
  CONSTRAINT permission_pkey PRIMARY KEY (id),
  CONSTRAINT user_permission_fkey FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

ALTER TABLE permissions OWNER TO app;

-- insert admin user
INSERT INTO users(id, login, passwd, is_superuser, disabled)
VALUES (1, 'admin', '$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD', TRUE, FALSE);
