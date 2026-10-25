"""Parse Python source into a structure the rules can inspect.

We never execute the code — only read its syntax tree.
"""

import ast


def parse_file(path):
    """Return (tree, source) for a Python file."""
    with open(path, encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source), source


def functions(tree):
    """Every function defined in the file (including nested ones)."""
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def function_info(fn):
    """The facts a rule usually needs about one function."""
    return {
        "name": fn.name,
        "params": [a.arg for a in fn.args.args],
        "line": fn.lineno,
        "node": fn,
    }


def calls_in(fn):
    """Every function call inside fn, as (called_name, lineno)."""
    out = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None)
            if name is None:
                name = getattr(node.func, "attr", None)
            if name:
                out.append((name, node.lineno))
    return out


def assignments_in(fn):
    """Every `name = ...` inside fn, as (target_name, lineno)."""
    out = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out.append((t.id, node.lineno))
    return out
