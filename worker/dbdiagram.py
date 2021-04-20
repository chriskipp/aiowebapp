#!/usr/bin/env python3

from sqlalchemy import create_engine, MetaData
from sadisplay import describe, render, __version__

url = 'postgresql://postgres:password@localhost:5432/app'

def dbdiagram(url):
    engine = create_engine(url)
    meta = MetaData()

    # Set schema(s) to reflect
    schema = 'public'
    if schema:
        pass
    else:
        schema = 'public'

    for s in schema.split(','):
        meta.reflect(bind=engine,schema=s)

    print('Database tables:')
    tables = sorted(meta.tables.keys())

    def _g(l, i):
        try:
            return tables[i]
        except IndexError:
            return ''

    for i in range(0, len(tables), 2):
        print(' {0}{1}{2}'.format(
            _g(tables, i),
            ' ' * (38 - len(_g(tables, i))),
            _g(tables, i + 1), ))

    tables = set(meta.tables.keys())

    exclude = []
    if exclude:
        tables -= set(map(str.strip, exclude.split(',')))

    desc = describe(
        map(lambda x: operator.getitem(meta.tables, x), sorted(tables)))
    return getattr(render, 'dot')(desc)

dbdiagram(url)
