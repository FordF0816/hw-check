"""Tests for the rules. Run with `pytest` or plain `python tests/test_rules.py`."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hw_check import check_source  # noqa: E402


def ids(issues):
    return sorted({i["id"] for i in issues})


# ------------------------------------------------------------------ rule 1


def test_correct_name_passes():
    src = "def sum_even_digits(n):\n    return n\n"
    assert 1 not in ids(check_source(src, spec="sum_even_digits"))


def test_wrong_name_fires():
    src = "def um_even_digits(n):\n    return n\n"
    assert 1 in ids(check_source(src, spec="sum_even_digits"))


def test_no_spec_skips_rule_1():
    src = "def anything(n):\n    return n\n"
    assert 1 not in ids(check_source(src))


# ------------------------------------------------------------------ rule 3


def test_param_overwritten_fires():
    src = "def f(times):\n    times = int(input())\n    return times\n"
    assert 3 in ids(check_source(src))


def test_local_variable_is_fine():
    src = "def f(times):\n    total = 0\n    return total\n"
    assert 3 not in ids(check_source(src))


# ------------------------------------------------------------------ rule 6


def test_print_inside_function_fires():
    src = "def f(n):\n    print(n)\n    return n\n"
    assert 6 in ids(check_source(src))


def test_return_is_fine():
    src = "def f(n):\n    return n\n"
    assert 6 not in ids(check_source(src))


# ------------------------------------------------------------------ rule 7


def test_print_with_commas_fires():
    src = "def f(a, b):\n    print(a, b)\n"
    assert 7 in ids(check_source(src))


def test_single_argument_print_is_fine():
    src = "def f(a):\n    print(a)\n"
    assert 7 not in ids(check_source(src))


# ------------------------------------------------------------------ rule 9


def test_init_returning_value_fires():
    src = "class C:\n    def __init__(self, x):\n        return x\n"
    assert 9 in ids(check_source(src))


def test_init_returning_none_is_fine():
    src = "class C:\n    def __init__(self, x):\n        self.x = x\n"
    assert 9 not in ids(check_source(src))


# ------------------------------------------------------------------ clean


def test_clean_solution_has_no_issues():
    src = (
        "def sum_even_digits(n):\n"
        "    total = 0\n"
        "    while n > 0:\n"
        "        n, r = divmod(n, 10)\n"
        "        if r % 2 == 0:\n"
        "            total = total + r\n"
        "    return total\n"
    )
    assert check_source(src, spec="sum_even_digits") == []


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  PASS  {name}")
            except AssertionError:
                failures += 1
                print(f"  FAIL  {name}")
    print()
    print("all passed" if failures == 0 else f"{failures} failed")
    sys.exit(1 if failures else 0)
