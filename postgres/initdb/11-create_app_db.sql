\c app

-- create users table
CREATE TABLE IF NOT EXISTS users
(
  id SERIAL,
  login CHARACTER VARYING(256) NOT NULL,
  passwd CHARACTER VARYING(256) NOT NULL,
  is_superuser BOOLEAN NOT NULL DEFAULT false,
  disabled BOOLEAN NOT NULL DEFAULT false,
  CONSTRAINT user_pkey PRIMARY KEY (id),
  CONSTRAINT user_login_key UNIQUE (login)
);

ALTER TABLE users OWNER TO app;

-- and permissions for them
CREATE TABLE IF NOT EXISTS permissions
(
  id SERIAL,
  user_id integer NOT NULL,
  perm_name character varying(64) NOT NULL,
  CONSTRAINT permission_pkey PRIMARY KEY (id),
  CONSTRAINT user_permission_fkey FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

ALTER TABLE permissions OWNER TO app;

-- insert some data
INSERT INTO users(login, passwd, is_superuser, disabled)
VALUES ('admin', '$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD', TRUE, FALSE);
INSERT INTO users(login, passwd, is_superuser, disabled)
VALUES ('moderator', '$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD', FALSE, FALSE);
INSERT INTO users(login, passwd, is_superuser, disabled)
VALUES ('user', '$5$rounds=535000$2kqN9fxCY6Xt5/pi$tVnh0xX87g/IsnOSuorZG608CZDFbWIWBr58ay6S4pD', FALSE, FALSE);

INSERT INTO permissions(user_id, perm_name)
VALUES (2, 'protected');
INSERT INTO permissions(user_id, perm_name)
VALUES (2, 'public');
INSERT INTO permissions(user_id, perm_name)
VALUES (3, 'public');