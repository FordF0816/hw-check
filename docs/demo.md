# Demo

The one-minute walkthrough used in the presentation. Run it from the repository
root.

## 0:00 — The claim

> The autograder only compares strings. This solution is logically correct and
> still scores zero.

```bash
hw-check examples/broken.py --spec sum_even_digits
```

Nine rules fire. `score: 1/10 — this may score 0`.

## 0:15 — Point at the first one

```
[ 1] Function name mismatch
     line 5: the spec asks for `sum_even_digits`,
             but the file defines ['um_even_digits', ...]
```

> One missing letter. The autograder imports `sum_even_digits`, gets an
> `ImportError`, and never runs the code.

## 0:30 — Point at the second one

```
[ 4] input() inside a function
     line 7: `um_even_digits` calls input();
             the autograder runs without a keyboard
```

> The argument was already passed in. Reading it again blocks forever.

## 0:40 — Fix them

```bash
hw-check examples/clean.py --spec sum_even_digits
```

```
all 10 checks passed

score: 10/10
```

Exit code is `0`, so it can sit in a pre-submit script.

## 0:50 — The close

```bash
pip install hw-check
hw-check my_solution.py --spec sum_even_digits
```

> Three seconds, before you submit — instead of finding out from a zero.

## Screen recording checklist

- [ ] Terminal font large enough to read at 1080p
- [ ] `--no-colour` off (keep the colours)
- [ ] Run `broken.py` first, then `clean.py`
- [ ] Show the exit code with `echo $?`
- [ ] Keep the whole thing under 70 seconds
