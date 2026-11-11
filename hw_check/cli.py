"""Command line entry point."""

import argparse
import json
import sys

from .parser import functions, parse_file
from .report import format_json, format_report
from .rules import TOTAL_RULES, Context, run_all

EXIT_OK = 0
EXIT_ISSUES = 1
EXIT_ERROR = 2


def build_parser():
    parser = argparse.ArgumentParser(
        prog="hw-check",
        description="Check whether a Python homework will score 0 on an autograder.",
    )
    parser.add_argument("file", help="the .py file to check")
    parser.add_argument(
        "--spec",
        metavar="NAME",
        action="append",
        default=None,
        help="the function name the question asks for, e.g. sum_even_digits. "
        "Repeat the flag to accept several names.",
    )
    parser.add_argument(
        "--json", action="store_true", help="print a machine-readable report"
    )
    parser.add_argument(
        "--no-colour",
        "--no-color",
        dest="no_colour",
        action="store_true",
        help="disable ANSI colours",
    )
    parser.add_argument(
        "--version", action="version", version="hw-check 0.2.0"
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    try:
        tree, source = parse_file(args.file)
    except FileNotFoundError:
        print(f"hw-check: no such file: {args.file}", file=sys.stderr)
        return EXIT_ERROR
    except SyntaxError as e:
        print(f"hw-check: cannot parse {args.file}: {e}", file=sys.stderr)
        return EXIT_ERROR

    specs = args.spec or []
    ctx = Context(funcs=functions(tree), tree=tree, source=source, specs=specs)
    issues = run_all(ctx)

    if args.json:
        print(
            json.dumps(
                format_json(args.file, issues, TOTAL_RULES, specs=specs), indent=2
            )
        )
    else:
        colour = not args.no_colour and sys.stdout.isatty()
        print(
            format_report(
                args.file, issues, TOTAL_RULES, colour=colour, specs=specs
            )
        )

    return EXIT_OK if not issues else EXIT_ISSUES


if __name__ == "__main__":
    raise SystemExit(main())
