import pytest
from migra import schemainspect
from migra.db import connect
from migra.schemainspect import NullInspector, get_inspector

from ._schemainspect_helpers import asserts_pg, setup_pg_schema


def test_postgres_inspect(db, pytestconfig):
    if pytestconfig.getoption("timescale"):
        pytest.skip("--timescale was specified")
    else:
        assert_postgres_inspect(db)


@pytest.mark.timescale
def test_timescale_inspect(db):
    assert_postgres_inspect(db, has_timescale=True)


def assert_postgres_inspect(db, has_timescale=False):
    with connect(db) as s:
        if has_timescale:
            s.execute("create extension if not exists timescaledb;")
        setup_pg_schema(s)
        i = get_inspector(s)
        asserts_pg(i, has_timescale)
        assert i == i == get_inspector(s)


def test_empty():
    x = NullInspector()
    assert x.tables == {}
    assert x.relations == {}
    assert type(schemainspect.get_inspector(None)) == NullInspector


def test_raw_connection(db):
    with connect(db) as s:
        setup_pg_schema(s)
        i1 = get_inspector(s)

    with connect(db) as s:
        i2 = get_inspector(s)

    assert i1 == i2
