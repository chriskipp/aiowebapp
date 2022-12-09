.load ./spellfix

-- Create a table. And an external content fts5 table to index it.

CREATE VIRTUAL TABLE 
IF NOT EXISTS "fts_idx"
USING fts5(
  "fingerprint" UNINDEXED
  , "url"
  , "title"
  , "text"
);


-- Create an fts5vocab "row" table to query the full-text index belonging
-- to FTS5 table "ft1".
CREATE VIRTUAL TABLE ft1_v USING fts5vocab('fts_idx', 'row');

-- Create an fts5vocab "col" table to query the full-text index belonging
-- to FTS5 table "ft2".
CREATE VIRTUAL TABLE ft2_v USING fts5vocab('fts_idx', 'col');

-- Create an fts5vocab "instance" table to query the full-text index
-- belonging to FTS5 table "ft3".
CREATE VIRTUAL TABLE ft3_v USING fts5vocab('fts_idx', 'instance');


CREATE VIRTUAL TABLE
IF NOT EXISTS fts_col
USING fts5vocab(
  fts_idx,
  "col"
);

CREATE virtual TABLE
IF NOT EXISTS spell
USING spellfix1;


INSERT INTO spell(word, rank)
SELECT DISTINCT term
  , SUM(cnt)
FROM fts_col
GROUP BY term;


