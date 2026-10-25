# hw-check

**Catch the mistakes that make an autograder score 0 — before you submit.**

---

## Why

The CS1302A autograder does exactly one thing: it compares what your program
prints against the expected string, character by character.

That means your logic can be completely correct and you still score **0**:

```
function name has a typo          → 0
one extra print()                 → 0
output on one line instead of 3   → 0
__init__ returns a value          → 0
```

Nothing checks for this. `pytest` checks logic. `flake8` checks style.
**No tool checks the autograder's own rules.**

`hw-check` does.

---

## Install

```bash
pip install hw-check
```

Python 3.9+. No dependencies — it uses `ast` from the standard library.

---

## Use

```bash
hw-check my_solution.py --spec sum_even_digits
```

```
checking my_solution.py

  [1] Function name mismatch
      line 1: the spec asks for `sum_even_digits`,
              but the file defines ['um_even_digits']

  [3] Parameter overwritten
      line 4: `times` is a parameter, but it is reassigned inside
              `f` — the value passed in is discarded

  3 of 5 checks passed

  score: 3/5  — this may score 0
```

Exit code is `0` when everything passes, `1` when something fires — so you can
drop it into a pre-submit script.

### From Python

```python
from hw_check import check_file

for issue in check_file("my_solution.py", spec="sum_even_digits"):
    print(issue["id"], issue["rule"], issue["detail"])
```

---

## What it checks

| # | Rule | Why it costs marks |
|---|---|---|
| 1 | **Function name mismatch** | the autograder calls a name that doesn't exist → 0 |
| 3 | **Parameter overwritten** | `times = int(input())` throws away the value that was passed in |
| 6 | **`print()` inside a function** | prints to the screen, returns `None` |
| 7 | **`print()` with several arguments** | puts everything on one line; expected output may be one value per line |
| 9 | **`__init__` returns a value** | `TypeError: __init__() should return None` |

**More rules are on the way** — see `hw_check/rules/__init__.py`. Adding one is
a single function plus a line in `ALL_RULES`.

---

## How it works

`hw-check` **parses** your file with `ast` and inspects the syntax tree.
It never executes your code.

That matters for three reasons:

- **Safe** — a solution with an infinite loop can still be checked
- **Fast** — no imports, no execution
- **Structural** — "this parameter is reassigned" is invisible at runtime,
  but obvious in the tree

---

## Adding a rule

```python
# hw_check/rules/__init__.py

def rule_my_check(funcs):
    issues = []
    for f in funcs:
        ...
    return issues

ALL_RULES = [..., rule_my_check]
```

An issue is a dict:

```python
{
    "id": 11,
    "rule": "Short title",
    "detail": "What is wrong and how to fix it",
    "line": 7,
}
```

---

## Roadmap

- [x] Rules 1, 3, 6, 7, 9
- [ ] Rules 2, 4, 5, 8, 10
- [ ] `--fix` suggestions
- [ ] Pre-commit hook

---

## Licence

MIT
