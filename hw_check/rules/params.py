"""Rules 3-5: the arguments the autograder passes must survive the call."""

from ..parser import assignments_in, calls_in, loaded_names
from .base import issue


def check_param_overwritten(ctx):
    """Rule 3: a parameter is assigned inside the function — the caller's value is lost."""
    issues = []
    for f in ctx.funcs:
        params = {a.arg for a in f.args.args}
        for name, line in assignments_in(f):
            if name in params and name != "self":
                issues.append(
                    issue(
                        3,
                        "Parameter overwritten",
                        f"`{name}` is a parameter, but it is reassigned inside "
                        f"`{f.name}` — the value passed in is discarded",
                        line,
                    )
                )
    return issues


def check_input_inside_function(ctx):
    """Rule 4: input() waits for a keystroke; the autograder has no keyboard."""
    issues = []
    for f in ctx.funcs:
        for name, line in calls_in(f):
            if name == "input":
                issues.append(
                    issue(
                        4,
                        "input() inside a function",
                        f"`{f.name}` calls input(); the autograder runs without a "
                        f"keyboard, so the call blocks or raises EOFError",
                        line,
                    )
                )
    return issues


def check_unused_parameter(ctx):
    """Rule 5: a parameter is never read — probably the wrong variable is used."""
    issues = []
    for f in ctx.funcs:
        params = [a.arg for a in f.args.args if a.arg != "self"]
        used = loaded_names(f)
        for name in params:
            if name not in used:
                issues.append(
                    issue(
                        5,
                        "Parameter never used",
                        f"`{name}` is a parameter of `{f.name}` but is never read "
                        f"inside the body — check that the right variable is used",
                        f.lineno,
                    )
                )
    return issues
