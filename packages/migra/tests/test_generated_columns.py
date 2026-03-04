from migra import Migration
from migra.db import connect, temporary_database
from migra.schemainspect import get_inspector


def test_generated_column_type():
    """Verify generated columns track generated_type and produce correct DDL."""
    with (
        temporary_database(host="localhost") as d0,
        temporary_database(host="localhost") as d1,
    ):
        with connect(d0) as s0, connect(d1) as s1:
            s0.execute("create table t(a int);")
            s1.execute("""
                create table t(
                    a int,
                    b int generated always as (a * 2) stored
                );
            """)

        with connect(d0) as s0, connect(d1) as s1:
            m = Migration(s0, s1)
            m.inspect_from()
            m.inspect_target()
            m.set_safety(False)
            m.add_all_changes()
            sql = m.sql.lower()
            assert "generated always as" in sql
            assert "stored" in sql


def test_generated_column_inspected():
    """Verify generated_type is correctly introspected from pg_attribute."""
    with temporary_database(host="localhost") as d0:
        with connect(d0) as s0:
            s0.execute("""
                create table t(
                    a int,
                    b int generated always as (a * 2) stored
                );
            """)
        with connect(d0) as s0:
            i = get_inspector(s0)
            cols = i.relations['"public"."t"'].columns
            assert cols["a"].generated_type is None
            assert cols["b"].generated_type == "s"
            assert cols["b"].is_generated is True
