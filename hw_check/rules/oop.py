"""Rules 9-10: the two ways __init__ quietly breaks an object."""

import ast

from ..parser import self_attributes
from .base import issue


def check_init_returns(ctx):
    """Rule 9: __init__ must not return a value."""
    issues = []
    for f in ctx.funcs:
        if f.name != "__init__":
            continue
        for node in ast.walk(f):
            if isinstance(node, ast.Return) and node.value is not None:
                issues.append(
                    issue(
                        9,
                        "__init__ returns a value",
                        "Python raises TypeError: __init__() should return None",
                        node.lineno,
                    )
                )
    return issues


def check_attribute_not_stored(ctx):
    """Rule 10: a parameter of __init__ is never stored on self."""
    issues = []
    for f in ctx.funcs:
        if f.name != "__init__":
            continue
        stored = self_attributes(f)
        for a in f.args.args:
            if a.arg == "self":
                continue
            if a.arg not in stored:
                issues.append(
                    issue(
                        10,
                        "Attribute never stored",
                        f"`{a.arg}` is a parameter of __init__ but `self.{a.arg}` "
                        f"is never assigned — the object will not have this attribute",
                        f.lineno,
                    )
                )
    return issues
