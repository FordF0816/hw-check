"""Parse Python source into a structure the rules can inspect.

We never execute the code — only read its syntax tree.
"""

import ast


def parse_file(path):
    """Return (tree, source) for a Python file."""
    with open(path, encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source), source


def parse_source(source):
    """Return a syntax tree for a string of Python source."""
    return ast.parse(source)


def functions(tree):
    """Every function defined in the file (including nested ones)."""
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def classes(tree):
    """Every class defined in the file."""
    return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


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


def call_nodes(fn, name):
    """Every call node inside fn whose callee is `name`."""
    out = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == name:
            out.append(node)
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


def self_attributes(fn):
    """Every attribute stored on self inside fn, e.g. {'w', 'h'} for self.w = w."""
    out = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if (
                    isinstance(t, ast.Attribute)
                    and isinstance(t.value, ast.Name)
                    and t.value.id == "self"
                ):
                    out.add(t.attr)
    return out


def loaded_names(fn):
    """Every name read (not written) inside fn."""
    return {
        n.id
        for n in ast.walk(fn)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
    }
