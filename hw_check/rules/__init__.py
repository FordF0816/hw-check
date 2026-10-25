"""Rules that catch mistakes which make an autograder score 0.

Each rule is a function `check(...)` returning a list of issues.
An issue is a dict: {"id", "rule", "detail", "line"}.

Adding a rule = adding a function here + registering it in __init__.py.
"""

from ..parser import calls_in, assignments_in


# ---------------------------------------------------------------- naming


def rule_function_name(funcs, spec_name=None):
    """Rule 1: the function the autograder calls must exist, with the exact name."""
    issues = []
    if not spec_name:
        return issues

    names = [f.name for f in funcs]
    if spec_name not in names:
        issues.append(
            {
                "id": 1,
                "rule": "Function name mismatch",
                "detail": f"the spec asks for `{spec_name}`, "
                f"but the file defines {names or 'nothing'}",
                "line": funcs[0].lineno if funcs else 0,
            }
        )
    return issues


# ---------------------------------------------------------------- params


def rule_param_overwritten(funcs):
    """Rule 3: a parameter is assigned inside the function — the caller's value is lost."""
    issues = []
    for f in funcs:
        params = {a.arg for a in f.args.args}
        for name, line in assignments_in(f):
            if name in params:
                issues.append(
                    {
                        "id": 3,
                        "rule": "Parameter overwritten",
                        "detail": f"`{name}` is a parameter, but it is reassigned "
                        f"inside `{f.name}` — the value passed in is discarded",
                        "line": line,
                    }
                )
    return issues


# ---------------------------------------------------------------- output


def rule_stray_print(funcs):
    """Rule 6: a function prints instead of returning."""
    issues = []
    for f in funcs:
        for name, line in calls_in(f):
            if name == "print":
                issues.append(
                    {
                        "id": 6,
                        "rule": "print() inside a function",
                        "detail": f"`{f.name}` prints; if the spec wants a return "
                        f"value, this prints to the screen and returns None",
                        "line": line,
                    }
                )
    return issues


def rule_print_with_commas(funcs):
    """Rule 7: print(a, b) puts everything on one line."""
    issues = []
    for f in funcs:
        for node in _walk_calls(f, "print"):
            if len(node.args) > 1:
                issues.append(
                    {
                        "id": 7,
                        "rule": "print() with several arguments",
                        "detail": "print(a, b) writes them on one line; "
                        "if the expected output is one value per line, use separate print() calls",
                        "line": node.lineno,
                    }
                )
    return issues


def _walk_calls(fn, name):
    import ast

    out = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == name:
            out.append(node)
    return out


# ---------------------------------------------------------------- oop


def rule_init_returns(funcs):
    """Rule 9: __init__ must not return a value."""
    import ast

    issues = []
    for f in funcs:
        if f.name != "__init__":
            continue
        for node in ast.walk(f):
            if isinstance(node, ast.Return) and node.value is not None:
                issues.append(
                    {
                        "id": 9,
                        "rule": "__init__ returns a value",
                        "detail": "Python raises TypeError: __init__() should return None",
                        "line": node.lineno,
                    }
                )
    return issues


ALL_RULES = [
    rule_function_name,
    rule_param_overwritten,
    rule_stray_print,
    rule_print_with_commas,
    rule_init_returns,
]
