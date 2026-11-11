# hw-check

**Catch the mistakes that make an autograder score 0 — before you submit.**

The CS1302A autograder compares your program's output against the expected
string, character by character. Correct logic still scores **0** if the
function name is misspelled, if a parameter is overwritten, or if the output
format differs.

`hw-check` reads your file's syntax tree and reports those mistakes. It never
runs your code, so it is safe even for a solution with an infinite loop.

## Install

```bash
pip install hw-check
```

Python 3.9 or newer. No third-party dependencies.

## First run

```bash
hw-check examples/broken.py --spec sum_even_digits
```

```
checking examples/broken.py  (spec: sum_even_digits)

  [ 1] Function name mismatch
       line 5: the spec asks for `sum_even_digits`, but the file defines
               ['um_even_digits', 'average', 'mean', '__init__']

  ...

  1 of 10 checks passed

  score: 1/10  — this may score 0
```

## Exit codes

| Code | Meaning |
|---|---|
| `0` | every check passed |
| `1` | at least one issue fired |
| `2` | the file is missing or cannot be parsed |

## Use it from Python

```python
from hw_check import check_file

for issue in check_file("solution.py", spec="sum_even_digits"):
    print(issue["id"], issue["rule"], issue["detail"])
```

## Where to go next

- [Rules](rules.md) — every check, with the mistake it catches
- [Demo](demo.md) — the one-minute walkthrough
