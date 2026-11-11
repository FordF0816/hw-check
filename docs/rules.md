# Rules

Ten checks. Each one corresponds to a mistake that has actually cost marks.

---

## 1. Function name mismatch

The autograder imports your file and calls the name written in the question.
One wrong letter and the import fails.

```python
# the question asks for sum_even_digits
def um_even_digits(n):     # ✗
    ...
```

```python
def sum_even_digits(n):    # ✓
    ...
```

---

## 2. No function defined

The file is a script: it runs from top to bottom and defines nothing. The
autograder has nothing to call.

```python
total = 0
for n in range(1, 11):
    total += n
print(total)               # ✗ no function at all
```

---

## 3. Parameter overwritten

The value the autograder passes in is discarded before it is ever used.

```python
def f(times):              # ✗
    times = int(input())
```

```python
def f(times):              # ✓
    ...
```

---

## 4. `input()` inside a function

The autograder runs without a keyboard. `input()` blocks forever or raises
`EOFError`.

```python
def f(n):                  # ✗
    n = int(input())
```

```python
def f(n):                  # ✓ the argument is already the data
    ...
```

---

## 5. Parameter never used

Usually means the wrong variable is being read — a silent wrong answer.

```python
def average(nums, weights):    # ✗ weights is never read
    return sum(nums) / len(nums)
```

---

## 6. `print()` inside a function

Printing sends text to the screen. If the question wants a `return` value, the
function returns `None` and the autograder sees nothing.

```python
def f(n):                  # ✗
    print(n * 2)
```

```python
def f(n):                  # ✓
    return n * 2
```

---

## 7. `print()` with several arguments

`print(a, b)` writes one line. If the expected output is one value per line,
this is a format mismatch — and a format mismatch is a zero.

```python
def f(a, b):               # ✗
    print(a, b)            # "1 2"
```

```python
def f(a, b):               # ✓
    print(a)
    print(b)
```

---

## 8. `round()` instead of fixed formatting

`round(20.0, 2)` returns `20.0`, not `20.00`. Fixed decimals are a formatting
problem, not a rounding problem.

```python
def mean(nums):            # ✗
    return round(sum(nums) / len(nums), 2)
```

```python
def mean(nums):            # ✓
    return f"{sum(nums) / len(nums):.2f}"
```

---

## 9. `__init__` returns a value

Python raises `TypeError: __init__() should return None`.

```python
class Counter:
    def __init__(self, name):
        return name        # ✗
```

---

## 10. Attribute never stored

`name = name` creates a local variable and throws it away. The object ends up
without the attribute, and every later `self.name` raises `AttributeError`.

```python
class Counter:
    def __init__(self, name):
        name = name        # ✗
```

```python
class Counter:
    def __init__(self, name):
        self.name = name   # ✓
```
