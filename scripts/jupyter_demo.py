"""Self-contained demo that runs anywhere `pip install hw-check` worked.

Paste one line into a JupyterHub cell:

    %run scripts/jupyter_demo.py

or, without the repository:

    import urllib.request; exec(urllib.request.urlopen(URL).read())

It writes a broken solution to a temporary file, checks it, then fixes it and
checks again, so the two scores appear side by side.
"""

import tempfile
from pathlib import Path

from hw_check import check_file
from hw_check.report import format_report
from hw_check.rules import TOTAL_RULES

BROKEN = '''\
def um_even_digits(times):
    total = 0
    times = int(input())
    while times > 0:
        times, r = divmod(times, 10)
        if r % 2 == 0:
            total = r + total
    print("the answer is", total)
    return total


class Counter:
    def __init__(self, name):
        name = name
        return name
'''

FIXED = '''\
def sum_even_digits(n):
    total = 0
    while n > 0:
        n, r = divmod(n, 10)
        if r % 2 == 0:
            total = total + r
    return total
'''


def run(label, source):
    with tempfile.NamedTemporaryFile(
        "w", suffix=".py", delete=False, encoding="utf-8"
    ) as fh:
        fh.write(source)
        path = fh.name

    issues = check_file(path, spec="sum_even_digits")
    print("=" * 62)
    print(label)
    print("=" * 62)
    print(format_report(path, issues, TOTAL_RULES, colour=False, specs=["sum_even_digits"]))
    Path(path).unlink()
    return len(issues)


def main():
    before = run("BEFORE - the student's first submission", BROKEN)
    after = run("AFTER - the same logic, structural mistakes fixed", FIXED)
    print()
    print(f"issues before: {before}   issues after: {after}")


if __name__ == "__main__":
    main()
