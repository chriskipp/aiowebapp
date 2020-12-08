import asyncio

from app.db import execute_sql, setup_pg, setup_pgsa, teardown_pg, teardown_pgsa
from app.main import create_app

loop = asyncio.get_event_loop()


async def test_dbsa_setup_teardown(loop=loop):
    app = create_app(loop)
    await setup_pgsa(app)
    assert "dbsa" in {k for k in app.keys()}
    await teardown_pgsa(app)
    assert app["dbsa"].closed


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


async def test_db_invalid_query(loop=loop):
    statement = """
        DROP erro FROM noch_mehr ERROR... test fail!;
    """
    app = create_app(loop)
    await setup_pg(app)

    res = await execute_sql(statement, app["db"])
    assert len(res) == 2
    assert res[0].decode() == statement
    assert res[1].__class__ != str
