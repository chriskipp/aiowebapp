#!/bin/sh

wget 'https://www.sqlite.org/src/tarball/sqlite.tar.gz'
tar -xf sqlite.tar.gz
cd sqlite

sed -i \
    -e '/^INCLUDE \.\.\/ext\/misc\/regexp.c$/a \/* @INCLUDE ./source.c *\/' \
    -e '/^    sqlite3_series_init(p->db, 0, 0)/a \/* @INIT_EXTENSIONS */' \
    ./src/shell.c.in

includefile() {
    sed -i \
        -e "/@INCLUDE/a INCLUDE ..\/ext\/misc\/${1}.c" \
        -e "/@INIT_EXTENSIONS/a    sqlite3_${1}_init(p->db, 0, 0);" \
        ./src/shell.c.in
}


CPPFLAGS="-DSQLITE_DEFAULT_MEMSTATUS=0 \
     -DSQLITE_DEFAULT_WAL_SYNCHRONOUS=1 \
     -DSQLITE_DEFAULT_SYNCHRONOUS=2 \
     -DSQLITE_LIKE_DOESNT_MATCH_BLOBS \
     -DSQLITE_MAX_EXPR_DEPTH=0 \
     -DSQLITE_OMIT_DEPRECATED \
     -DSQLITE_OMIT_SHARED_CACHE \
     -DHAVE_LOCALTIME_R \
     -DHAVE_MALLOC_USABLE_SIZE \
     -DHAVE_USLEEP=1 \
     -DHAVE_UTIME=1 \
     -DHAVE_READLINE \
     -DHAVE_EDITLINE \
     -DSQLITE_DEFAULT_AUTOMATIC_INDEX=1 \
     -DSQLITE_DEFAULT_AUTOVACUUM=2 \
     -DSQLITE_DEFAULT_FILE_PERMISSIONS=0600 \
     -DSQLITE_DEFAULT_FOREIGN_KEYS=1 \
     -DSQLITE_ENABLE_COLUMN_METADATA \
     -DSQLITE_ENABLE_FTS3 \
     -DSQLITE_ENABLE_FTS3_PARENTHESIS \
     -DSQLITE_ENABLE_FTS3_TOKENIZER \
     -DSQLITE_ENABLE_FTS4 \
     -DSQLITE_ENABLE_FTS5 \
     -DSQLITE_ENABLE_GEOPOLY \
     -DSQLITE_ENABLE_IOTRACE \
     -DSQLITE_ENABLE_MATH_FUNCTIONS \
     -DSQLITE_ENABLE_JSON1 \
     -DSQLITE_ENABLE_MEMORY_MANAGEMENT \
     -DSQLITE_ENABLE_MEMSYS5 \
     -DSQLITE_ENABLE_NORMALIZE \
     -DSQLITE_ENABLE_PREUPDATE_HOOK \
     -DSQLITE_ENABLE_RBU \
     -DSQLITE_ENABLE_RTREE=1 \
     -DSQLITE_ENABLE_SESSION \
     -DSQLITE_ENABLE_SNAPSHOT \
     -DSQLITE_ENABLE_SORTER_REFERENCES \
     -DSQLITE_ENABLE_STMTVTAB \
     -DSQLITE_ENABLE_STAT4 \
     -DSQLITE_ENABLE_UPDATE_DELETE_LIMIT \
     -DSQLITE_ENABLE_UNKNOWN_SQL_FUNCTION \
     -DSQLITE_ENABLE_UNLOCK_NOTIFY \
     -DSQLITE_ENABLE_UNLOCK_NOTIFY \
     -DSQLITE_THREADSAFE=1 \
     -DSQLITE_TEMP_STORE=2 \
     -DSQLITE_TRUSTED_SCHEMA=0 \
     -DSQLITE_USE_URI \
     -DSQLITE_ALLOW_URI_AUTHORITY \
     -DSQLITE_ENABLE_API_ARMOR \
     -DSQLITE_ENABLE_ATOMIC_WRITE \
     -DSQLITE_ENABLE_BATCH_ATOMIC_WRITE \
     -DSQLITE_ENABLE_BYTECODE_VTAB \
     -DSQLITE_ENABLE_DBPAGE_VTAB \
     -DSQLITE_ENABLE_DBSTAT_VTAB \
     -DSQLITE_INTROSPECTION_PRAGMAS \
     -DSQLITE_SOUNDEX \
     -DSQLITE_USE_ALLOCA \
     -DSQLITE_USE_FCNTL_TRACE \
     -DSQLITE_HAVE_ZLIB \
     -DSQLITE_ENABLE_DBPAGE_VTAB \
     -DSQLITE_ENABLE_DBSTAT_VTAB \
     -O2 -fPIC " ./configure \
          --enable-amalgamation --enable-editline \
          --enable-fts3 --enable-fts4 --enable-fts5 --enable-gcov \
          --enable-geopoly --enable-json --enable-largefile \
          --enable-load-extension --enable-math --enable-memsys5 \
          --enable-readline --enable-releasemode --enable-rtree \
          --enable-session --enable-shared=yes --enable-static=yes \
          --enable-tcl --enable-tempstore --enable-threadsafe \
          --enable-update-limit
for EXTENSION in spellfix; do
#      amatch anycollseq appendvfs blobio btreeinfo carray \
#      cksumvfs closure completion compress csv dbdata decimal eval explain \
#      fileio fossildelta fuzzer ieee754 memstat memvfs nextchar noop \
#      percentile prefixes qpvtab regexp remember rot13 series sha1 shathree \
#      showauth spellfix sqlar stmt templatevtab totype uint unionvtab urifuncs \
#      uuid vfsstat vtablog vtshim wholenumber zipfile zorder; do
      echo ${EXTENSION}
      includefile ${EXTENSION}
done
make
make install
cd -

rm -rf sqlite sqlite.tar.gz
