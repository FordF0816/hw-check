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
round(x, 2) instead of f"{x:.2f}" → 0
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
checking my_solution.py  (spec: sum_even_digits)

  [ 1] Function name mismatch
       line 3: the spec asks for `sum_even_digits`,
               but the file defines ['um_even_digits']

  [ 3] Parameter overwritten
       line 4: `times` is a parameter, but it is reassigned inside
               `f` — the value passed in is discarded

  8 of 10 checks passed

  score: 8/10  — this may score 0
```

### Several acceptable names

Repeat the flag; the check passes when **any** of them is defined.

```bash
hw-check solution.py --spec sum_even_digits --spec sum_even
```

### Machine-readable output

```bash
hw-check solution.py --spec sum_even_digits --json
```

```json
{
  "file": "solution.py",
  "specs": ["sum_even_digits"],
  "total_rules": 10,
  "passed": 8,
  "failed": 2,
  "issues": [
    {
      "id": 1,
      "rule": "Function name mismatch",
      "detail": "the spec asks for `sum_even_digits`, but the file defines ['um_even_digits']",
      "line": 3
    }
  ]
}
```

### Exit codes

| Code | Meaning |
|---|---|
| `0` | every check passed |
| `1` | at least one issue fired |
| `2` | the file is missing or cannot be parsed |

That makes it usable in a pre-submit script:

```bash
hw-check solution.py --spec sum_even_digits || echo "fix the issues above"
```

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
| 2 | **No function defined** | the file is a script; there is nothing to call |
| 3 | **Parameter overwritten** | `times = int(input())` throws away the value that was passed in |
| 4 | **`input()` inside a function** | the autograder has no keyboard; the call blocks or raises `EOFError` |
| 5 | **Parameter never used** | usually means the wrong variable is being read |
| 6 | **`print()` inside a function** | prints to the screen, returns `None` |
| 7 | **`print()` with several arguments** | puts everything on one line; expected output may be one value per line |
| 8 | **`round()` instead of fixed formatting** | `round(20.0, 2)` gives `20.0`, not `20.00` |
| 9 | **`__init__` returns a value** | `TypeError: __init__() should return None` |
| 10 | **Attribute never stored** | `name = name` instead of `self.name = name`; the attribute does not exist |

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

Write a function in `hw_check/rules/` that takes a `Context` and returns issues:

```python
# hw_check/rules/output.py

def check_something(ctx):
    issues = []
    for f in ctx.funcs:
        ...
    return issues
```

Then register it in `hw_check/rules/__init__.py`:

```python
Rule(11, "Short title", output.check_something),
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

## Layout

```
hw_check/
├─ __init__.py        public API: check_file / check_source
├─ cli.py             command line entry point
├─ parser.py          ast helpers (never executes code)
├─ report.py          text and JSON reports
└─ rules/
   ├─ __init__.py     the registry: ALL_RULES
   ├─ base.py         Context, Rule, issue
   ├─ naming.py       rules 1-2
   ├─ params.py       rules 3-5
   ├─ output.py       rules 6-8
   └─ oop.py          rules 9-10
```

---

## Development

```bash
git clone https://github.com/FordF0816/hw-check
cd hw-check
pip install -e ".[dev]"
python tests/test_rules.py        # or: pytest
mkdocs serve                      # docs at http://127.0.0.1:8000
```

---

## Roadmap

- [x] Rules 1–10
- [x] `--json`, exit codes, several `--spec` names
- [x] Documentation site
- [ ] `--fix` suggestions
- [ ] Pre-commit hook

---

## Licence

MIT
