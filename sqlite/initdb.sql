PRAGMA journal_mode=WAL;

CREATE TABLE
IF NOT EXISTS map (
      rowid INTEGER PRIMARY KEY,
      fingerprint TEXT,
      url TEXT,
      title TEXT,
      text TEXT
);

CREATE VIRTUAL TABLE
IF NOT EXISTS fts USING fts5(
  fingerprint UNINDEXED,
  url,
  title,
  text,
  content='',
  columnsize=1,
  detail=full
);

CREATE VIRTUAL TABLE
IF NOT EXISTS fts_row USING fts5vocab(
  'fts', 'row'
);

CREATE VIRTUAL TABLE
IF NOT EXISTS fts_col USING fts5vocab(
  'fts', 'col'
);

CREATE VIRTUAL TABLE
IF NOT EXISTS fts_inst USING fts5vocab(
  'fts', 'instance'
);

CREATE virtual TABLE
IF NOT EXISTS spell
USING spellfix1;


INSERT INTO spell(word, rank)
SELECT
  term,
  SUM(cnt)
FROM fts_col
GROUP BY term;


-- SELECT map.rowid, map.url, map.title
-- FROM fts
-- INNER JOIN map ON fts.rowid = map.rowid
-- WHERE fts MATCH 'url'
-- ;
