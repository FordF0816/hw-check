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

from .parser import parse_file, functions
from .rules import ALL_RULES

__version__ = "0.1.0"

__all__ = ["check_file", "check_source", "__version__"]


def check_source(source, spec=None):
    """Check Python source given as a string. Returns a list of issues."""
    import ast

    tree = ast.parse(source)
    funcs = functions(tree)
    return _run_rules(funcs, spec)


def check_file(path, spec=None):
    """Check a .py file. Returns a list of issues."""
    tree, _ = parse_file(path)
    funcs = functions(tree)
    return _run_rules(funcs, spec)


def _run_rules(funcs, spec):
    issues = []
    for rule in ALL_RULES:
        if rule.__name__ == "rule_function_name":
            issues.extend(rule(funcs, spec_name=spec))
        else:
            issues.extend(rule(funcs))
    issues.sort(key=lambda i: (i["line"], i["id"]))
    return issues
