from reprlib import recursive_repr

DQ = '"'


class AutoRepr:  # pragma: no cover
    @recursive_repr()
    def __repr__(self):
        done = set()

        cname = self.__class__.__name__

        vals = []
        for k in sorted(dir(self)):
            v = getattr(self, k)

            if not k.startswith("_") and (not callable(v)) and id(v) not in done:
                done.add(id(v))

                attr = f"{k}={v!r}"

                vals.append(attr)
        return f"{cname}({', '.join(vals)})"

    def __str__(self):
        return repr(self)

    def __ne__(self, other):
        return not self == other


def unquoted_identifier(identifier, *, schema=None, identity_arguments=None):
    if identifier is None and schema is not None:
        return schema
    s = str(identifier)
    if schema:
        s = f"{schema}.{s}"
    if identity_arguments is not None:
        s = f"{s}({identity_arguments})"
    return s


def quoted_identifier(identifier, schema=None, identity_arguments=None):
    if identifier is None and schema is not None:
        return f"{DQ}{schema.replace(DQ, DQ * 2)}{DQ}"
    s = f"{DQ}{identifier.replace(DQ, DQ * 2)}{DQ}"
    if schema:
        s = f"{DQ}{schema.replace(DQ, DQ * 2)}{DQ}.{s}"
    if identity_arguments is not None:
        s = f"{s}({identity_arguments})"
    return s
