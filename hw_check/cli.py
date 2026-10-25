"""Command line entry point."""

import argparse
import sys

from .parser import parse_file, functions
from .report import format_report
from .rules import ALL_RULES


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="hw-check",
        description="Check whether a Python homework will score 0 on an autograder.",
    )
    parser.add_argument("file", help="the .py file to check")
    parser.add_argument(
        "--spec",
        metavar="NAME",
        help="the function name the question asks for, e.g. sum_even_digits",
    )
    parser.add_argument(
        "--no-colour", action="store_true", help="disable ANSI colours"
    )
    args = parser.parse_args(argv)

    try:
        tree, _ = parse_file(args.file)
    except FileNotFoundError:
        print(f"hw-check: no such file: {args.file}", file=sys.stderr)
        return 2
    except SyntaxError as e:
        print(f"hw-check: cannot parse {args.file}: {e}", file=sys.stderr)
        return 2

    funcs = functions(tree)

    issues = []
    for rule in ALL_RULES:
        if rule.__name__ == "rule_function_name":
            issues.extend(rule(funcs, spec_name=args.spec))
        else:
            issues.extend(rule(funcs))

    issues.sort(key=lambda i: (i["line"], i["id"]))
    print(format_report(args.file, issues, len(ALL_RULES), colour=not args.no_colour))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
