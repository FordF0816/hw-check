"""hw-check — catch the mistakes that make an autograder score 0.

The CS1302A autograder compares printed output against the expected string,
character by character. Correct logic still scores 0 if the function name is
misspelled, if a parameter is overwritten, or if the output format differs.

This package checks those things statically, without running the code.

    from hw_check import check_file

    issues = check_file("my_solution.py", spec="sum_even_digits")
    for issue in issues:
        print(issue["id"], issue["rule"], issue["detail"])
"""

from .parser import functions, parse_file, parse_source
from .rules import TOTAL_RULES, Context, run_all

__version__ = "0.2.0"

__all__ = ["check_file", "check_source", "TOTAL_RULES", "__version__"]


def _as_specs(spec=None, specs=None):
    if specs is not None:
        return list(specs)
    if spec is None:
        return []
    if isinstance(spec, str):
        return [spec]
    return list(spec)


def check_source(source, spec=None, specs=None):
    """Check Python source given as a string. Returns a list of issues."""
    tree = parse_source(source)
    ctx = Context(
        funcs=functions(tree),
        tree=tree,
        source=source,
        specs=_as_specs(spec, specs),
    )
    return run_all(ctx)


def check_file(path, spec=None, specs=None):
    """Check a .py file. Returns a list of issues."""
    tree, source = parse_file(path)
    ctx = Context(
        funcs=functions(tree),
        tree=tree,
        source=source,
        specs=_as_specs(spec, specs),
    )
    return run_all(ctx)
