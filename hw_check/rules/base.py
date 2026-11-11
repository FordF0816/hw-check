"""Shared plumbing: the context every rule receives, and the issue shape."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Context:
    """Everything a rule may need, computed once per file."""

    funcs: List[object]
    tree: object
    source: str
    specs: List[str] = field(default_factory=list)


def issue(rule_id: int, title: str, detail: str, line: int):
    """One finding. The shape is part of the public API — keep it stable."""
    return {"id": rule_id, "rule": title, "detail": detail, "line": line}


@dataclass(frozen=True)
class Rule:
    """A rule is an id, a title, and a function from Context to issues."""

    id: int
    title: str
    check: object
    needs_spec: bool = False
