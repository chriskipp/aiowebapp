import pytest

from app.db import (
    execute_sql,
    fetch_sql,
    setup_pg,
    setup_pgsa,
    teardown_pg,
    teardown_pgsa,
)
from app.main import create_app


@pytest.fixture()
async def create_app_with_db():
    app = create_app()
    await setup_pg(app)
    yield app
    await teardown_pg(app)


@pytest.fixture()
async def create_app_with_dbsa():
    app = create_app()
    await setup_pgsa(app)
    app["db"] = app["dbsa"]
    yield app
    await teardown_pgsa(app)
    assert app["dbsa"].closed


async def test_dbsa_setup_teardown(create_app_with_dbsa):
    app = create_app_with_dbsa
    assert "dbsa" in app.keys()
    await teardown_pgsa(app)
    assert app["dbsa"].closed


@pytest.mark.asyncio
async def test_db_setup_teardown(create_app_with_db):
    app = create_app_with_db
    assert "db" in app.keys()


@pytest.mark.asyncio
async def test_db_create_table(create_app_with_db):
    create_statement = """
            CREATE TABLE test (
              a INTEGER,
              b FLOAT,
              c VARCHAR
            );"""
    app = create_app_with_db

    await execute_sql("DROP TABLE IF EXISTS test;", app["db"])
    res = await execute_sql(create_statement, app["db"])
    assert res == "CREATE TABLE"


@pytest.mark.asyncio
async def test_db_insert_into(create_app_with_db):
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
    app = create_app_with_db

    for i in range(len(items)):
        res = await execute_sql(statement.format(str(items[i])), app["db"])
        assert res == "INSERT 0 1"


@pytest.mark.asyncio
async def test_db_select(create_app_with_db):
    items = [
        {"a": 1, "b": 1.0, "c": "a"},
        {"a": 2, "b": 2.0, "c": "b"},
        {"a": 3, "b": 3.0, "c": "c"},
    ]
    statement = """
            SELECT *
            FROM test;
    """
    app = create_app_with_db

    res = await fetch_sql(statement, app["db"])
    assert res == items


@pytest.mark.asyncio
async def test_db_update(create_app_with_db):
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
        SELECT *
        FROM test;
    """
    app = create_app_with_db

    res = await execute_sql(update_statement, app["db"])
    assert res == "UPDATE 1"

    res = await fetch_sql(select_statement, app["db"])
    assert res == items


@pytest.mark.asyncio
async def test_db_delete(create_app_with_db):
    items = [
        {"a": 1, "b": 1.0, "c": "a"},
        {"a": 2, "b": 2.0, "c": "b"},
    ]
    delete_statement = """
        DELETE FROM test
        WHERE c = 'c';
    """
    select_statement = """
        SELECT *
        FROM test;
    """
    app = create_app_with_db

    res = await execute_sql(delete_statement, app["db"])
    assert res == "DELETE 1"

    res = await fetch_sql(select_statement, app["db"])
    assert res == items


@pytest.mark.asyncio
async def test_db_drop_table(create_app_with_db):
    statement = """
        DROP TABLE test;
    """
    app = create_app_with_db

    res = await execute_sql(statement, app["db"])
    assert res == "DROP TABLE"


@pytest.mark.asyncio
async def test_db_invalid_query(create_app_with_db):
    statement = """
        DROP error
        FROM noch_mehr_error
        ... test fail!;
    """
    app = create_app_with_db

    res = await execute_sql(statement, app["db"])
    assert res.__class__ != str
