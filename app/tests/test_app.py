import asyncio
import logging

from aiohttp import web

from app.db import execute_sql, setup_pg, teardown_pg
from app.main import create_app
from app.redis import (
    del_redis_key,
    get_redis_json,
    get_redis_key,
    set_redis_json,
    set_redis_key,
    setup_redis,
    teardown_redis,
)

loop = asyncio.get_event_loop()


async def test_app_creation(loop=loop):
    app = create_app(loop)
    app2 = web.Application()
    assert type(app) == type(app)


async def test_app_logger(loop=loop) -> None:
    app = create_app(loop)
    assert type(app.logger) is logging.Logger
    assert app.logger.disabled == False


async def test_index(aiohttp_client):
    client = await aiohttp_client(create_app)
    resp = await client.get("/")
    assert resp.status == 200


async def test_redis_setup_teardown(loop=loop):
    app = create_app(loop)
    await setup_redis(app)
    assert "redis" in {k for k in app.keys()}
    await teardown_redis(app)
    assert app["redis"].closed


async def test_redis_keys(loop=loop):
    app = create_app(loop)
    await setup_redis(app)

    await set_redis_key(app["redis"], "test_key", "test_value")
    v = await get_redis_key(app["redis"], "test_key")
    assert v == "test_value"
    await del_redis_key(app["redis"], "test_key")
    v = await get_redis_key(app["redis"], "test_key")
    assert v == None


async def test_redis_set_json(loop=loop):
    json_obj = {"a": 1, "b": 2, "c": 3}
    app = create_app(loop)
    await setup_redis(app)

    await set_redis_json(app["redis"], "test_obj", json_obj)
    res = await get_redis_json(app["redis"], "test_obj")
    assert res == json_obj


async def test_redis_modules(loop=loop):
    app = create_app(loop)
    await setup_redis(app)

    pool = app["redis"]
    modules = await pool.execute("MODULE", "LIST")
    modules = {m[1].decode() for m in modules}
    assert "ReJSON" in modules
    assert "search" in modules


async def test_db_setup_teardown(loop=loop):
    app = create_app(loop)
    await setup_pg(app)
    assert "db" in {k for k in app.keys()}
    await teardown_pg(app)
    assert app["db"].closed


async def test_db_create_table(loop=loop):
    statement = """
            CREATE TABLE test (
              a INTEGER,
              b FLOAT,
              c VARCHAR
            );"""
    app = create_app(loop)
    await setup_pg(app)

    await execute_sql("DROP TABLE IF EXISTS test;", app["db"])
    res = await execute_sql(statement, app["db"])
    assert len(res) == 2
    assert res[0].decode() == statement
    assert res[1] == "CREATE TABLE"


async def test_db_insert_into(loop=loop):
    items = [
        (1, 1.0, "a"),
        (2, 2.0, "b"),
        (3, 3.0, "c"),
    ]
    statement = """
            INSERT INTO test (
              a, b, c
            ) VALUES 
              {}
            ;"""
    app = create_app(loop)
    await setup_pg(app)

    for i in range(len(items)):
        res = await execute_sql(statement.format(str(items[i])), app["db"])
        assert len(res) == 2
        assert res[0].decode() == statement.format(str(items[i]))
        assert res[1] == "INSERT 0 1"


async def test_db_select(loop=loop):
    items = [
        {"a": 1, "b": 1.0, "c": "a"},
        {"a": 2, "b": 2.0, "c": "b"},
        {"a": 3, "b": 3.0, "c": "c"},
    ]
    statement = """
            SELECT *
            FROM test;
    """
    app = create_app(loop)
    await setup_pg(app)

    res = await execute_sql(statement, app["db"])
    assert len(res) == 3
    assert res == items


async def test_db_update(loop=loop):
    items = [
        {"a": 1, "b": 1.0, "c": "a"},
        {"a": 2, "b": 2.0, "c": "b"},
        {"a": 4, "b": 3.0, "c": "c"},
    ]
    update_statement = """
        UPDATE test
        SET a = 4
        WHERE c = 'c';
    """
    select_statement = """
        SELECT * FROM test;
    """
    app = create_app(loop)
    await setup_pg(app)

    res = await execute_sql(update_statement, app["db"])
    assert len(res) == 2
    assert res[0].decode() == update_statement
    assert res[1] == "UPDATE 1"

    res = await execute_sql(select_statement, app["db"])
    assert len(res) == 3
    assert res == items


async def test_db_delete(loop=loop):
    items = [
        {"a": 1, "b": 1.0, "c": "a"},
        {"a": 2, "b": 2.0, "c": "b"},
    ]
    delete_statement = """
        DELETE FROM test
        WHERE c = 'c';
    """
    select_statement = """
        SELECT * FROM test;
    """
    app = create_app(loop)
    await setup_pg(app)

    res = await execute_sql(delete_statement, app["db"])
    assert len(res) == 2
    assert res[0].decode() == delete_statement
    assert res[1] == "DELETE 1"

    res = await execute_sql(select_statement, app["db"])
    assert len(res) == 2
    assert res == items


async def test_db_drop_table(loop=loop):
    statement = """
        DROP TABLE test;
    """
    app = create_app(loop)
    await setup_pg(app)

    res = await execute_sql(statement, app["db"])
    assert len(res) == 2
    assert res[0].decode() == statement
    assert res[1] == "DROP TABLE"
