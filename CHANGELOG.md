# Changelog

## 0.2.0

All ten rules, a machine-readable report, and a documentation site.

### Added
- Rules 2, 4, 5, 8, 10 — the set is now complete.
- `--json` for machine-readable output.
- `--spec` may be repeated; the check passes when any listed name is defined.
- `--version`.
- Exit code `2` for an unreadable or unparsable file.
- Documentation site (`mkdocs.yml`, `docs/`).
- `examples/no_function.py`, to demonstrate rule 2.
- `CHANGELOG.md`.

### Changed
- `hw_check/rules/` is now a package: `naming.py`, `params.py`, `output.py`,
  `oop.py`, plus a registry in `__init__.py`.
- Every rule receives one `Context` object instead of ad-hoc arguments.
- Colours are enabled only when stdout is a terminal.
- `check_file` / `check_source` accept `specs=[...]` as well as `spec=...`.

### Fixed
- Rule 1 no longer reports a missing function when the file defines nothing —
  rule 2 has the clearer message.

## 0.1.0

First working version.

- Rules 1, 3, 6, 7, 9.
- `hw-check file.py --spec name`.
- Text report with a score out of the number of rules.
- Unit tests runnable with `pytest` or `python tests/test_rules.py`.
