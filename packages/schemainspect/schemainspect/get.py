from .inspector import NullInspector
from .pg import PostgreSQL


def get_inspector(x, schema=None, exclude_schema=None):
    if schema and exclude_schema:
        raise ValueError("Cannot provide both schema and exclude_schema")
    if x is None:
        return NullInspector()

    inspected = PostgreSQL(x)
    if schema:
        inspected.one_schema(schema)
    elif exclude_schema:
        inspected.exclude_schema(exclude_schema)
    return inspected
