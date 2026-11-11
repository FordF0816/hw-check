"""Rules 1-2: the function the autograder calls must exist, spelled exactly."""

from .base import issue


def check_name_mismatch(ctx):
    """Rule 1: there are functions, but none has the name the question asked for."""
    if not ctx.specs:
        return []

    names = [f.name for f in ctx.funcs]
    if any(spec in names for spec in ctx.specs):
        return []
    if not names:
        return []  # rule 2 reports this case, with a clearer message

    wanted = " / ".join(f"`{s}`" for s in ctx.specs)
    return [
        issue(
            1,
            "Function name mismatch",
            f"the spec asks for {wanted}, but the file defines {names}",
            ctx.funcs[0].lineno,
        )
    ]


def check_no_function(ctx):
    """Rule 2: the file defines no function at all — the autograder has nothing to call."""
    if not ctx.specs or ctx.funcs:
        return []

    wanted = " / ".join(f"`{s}`" for s in ctx.specs)
    return [
        issue(
            2,
            "No function defined",
            f"the spec asks for {wanted}, but the file defines no function at all "
            f"— the autograder calls a name that does not exist",
            1,
        )
    ]
