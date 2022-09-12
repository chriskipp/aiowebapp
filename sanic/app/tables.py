#!/usr/bin/env python3

import hashlib

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID


def get_fingerprint(url):
    m = hashlib.md5()
    m.update(url.encode())
    return m.digest().hex()


metadata = sqlalchemy.MetaData()


class URL(Base):
    __tablename__ = "urls"
    fingerprint = sqlalchemy.Column(UUID(), primary_key=True)
    url = (sqlalchemy.Column(sqlalchemy.String()),)
    title = sqlalchemy.Column(sqlalchemy.String(length=100))


urls = sqlalchemy.Table()
