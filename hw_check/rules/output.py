"""Rules 6-8: the autograder compares printed text, so the shape of the output matters."""

from ..parser import call_nodes, calls_in
from .base import issue


def check_stray_print(ctx):
    """Rule 6: a function prints instead of returning."""
    issues = []
    for f in ctx.funcs:
        for name, line in calls_in(f):
            if name == "print":
                issues.append(
                    issue(
                        6,
                        "print() inside a function",
                        f"`{f.name}` prints; if the spec wants a return value, "
                        f"this prints to the screen and returns None",
                        line,
                    )
                )
    return issues


def check_print_with_commas(ctx):
    """Rule 7: print(a, b) puts everything on one line."""
    issues = []
    for f in ctx.funcs:
        for node in call_nodes(f, "print"):
            if len(node.args) > 1:
                issues.append(
                    issue(
                        7,
                        "print() with several arguments",
                        "print(a, b) writes them on one line; if the expected "
                        "output is one value per line, use separate print() calls",
                        node.lineno,
                    )
                )
    return issues


def check_round_instead_of_format(ctx):
    """Rule 8: round(x, 2) returns a float, so trailing zeros disappear."""
    issues = []
    for f in ctx.funcs:
        for node in call_nodes(f, "round"):
            if len(node.args) == 2:
                issues.append(
                    issue(
                        8,
                        "round() instead of fixed formatting",
                        "round(20.0, 2) gives 20.0, not 20.00 — if the expected "
                        'output has fixed decimals, use f"{x:.2f}"',
                        node.lineno,
                    )
                )
    return issues
