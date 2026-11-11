"""The rule registry.

Adding a rule takes two lines: write a function `check_*(ctx)` in one of the
modules, then add a `Rule(...)` entry to ALL_RULES below.
"""

from .base import Context, Rule, issue
from . import naming, oop, output, params

ALL_RULES = [
    Rule(1, "Function name mismatch", naming.check_name_mismatch, needs_spec=True),
    Rule(2, "No function defined", naming.check_no_function, needs_spec=True),
    Rule(3, "Parameter overwritten", params.check_param_overwritten),
    Rule(4, "input() inside a function", params.check_input_inside_function),
    Rule(5, "Parameter never used", params.check_unused_parameter),
    Rule(6, "print() inside a function", output.check_stray_print),
    Rule(7, "print() with several arguments", output.check_print_with_commas),
    Rule(8, "round() instead of fixed formatting", output.check_round_instead_of_format),
    Rule(9, "__init__ returns a value", oop.check_init_returns),
    Rule(10, "Attribute never stored", oop.check_attribute_not_stored),
]

RULES_BY_ID = {rule.id: rule for rule in ALL_RULES}

TOTAL_RULES = len(ALL_RULES)


def run_all(ctx):
    """Run every rule and return the issues sorted by line, then by rule id."""
    issues = []
    for rule in ALL_RULES:
        issues.extend(rule.check(ctx))
    issues.sort(key=lambda i: (i["line"], i["id"]))
    return issues


__all__ = ["ALL_RULES", "RULES_BY_ID", "TOTAL_RULES", "Context", "Rule", "issue", "run_all"]
