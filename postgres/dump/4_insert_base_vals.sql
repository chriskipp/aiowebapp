--==========================================================
-- Inserts common URL schemes
--==========================================================

\c weblog weblog

--==========================================================
-- Inserts common URL schemes
--==========================================================
INSERT INTO scheme (scheme) VALUES ('https');
INSERT INTO scheme (scheme) VALUES ('http');
INSERT INTO scheme (scheme) VALUES ('socks4');
INSERT INTO scheme (scheme) VALUES ('socks5');

--==========================================================
-- Inserts 'www.' and '' (empty string) domain prefix
--==========================================================
INSERT INTO www (www) VALUES ('');
INSERT INTO www (www) VALUES ('www.');

