#!/usr/bin/env python3

from sanic_envconfig import EnvConfig


class Settings(EnvConfig):
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000


#    DB_URL: 'sqlite+aiosqlite:////var/sqlite/index.sqlite'
