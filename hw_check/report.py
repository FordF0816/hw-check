"""Turn a list of issues into something a human wants to read."""

# ANSI colours — disabled automatically when output is piped
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def _paint(text, colour, enabled):
    return f"{colour}{text}{RESET}" if enabled else text


def format_report(path, issues, total_rules, colour=True):
    lines = []
    passed = total_rules - len({i["id"] for i in issues})

    lines.append("")
    lines.append(f"{_paint('checking', DIM, colour)} {path}")
    lines.append("")

    if not issues:
        lines.append(_paint(f"  all {total_rules} checks passed", GREEN, colour))
        lines.append("")
        lines.append(_paint(f"  score: {total_rules}/{total_rules}", BOLD, colour))
        return "\n".join(lines)

    for issue in issues:
        lines.append(
            _paint(f"  [{issue['id']}] {issue['rule']}", RED, colour)
        )
        lines.append(f"      line {issue['line']}: {issue['detail']}")
        lines.append("")

    lines.append(_paint(f"  {passed} of {total_rules} checks passed", YELLOW, colour))
    lines.append("")
    score = f"  score: {passed}/{total_rules}"
    if passed < total_rules:
        lines.append(_paint(score, BOLD, colour) + "  — this may score 0")
    else:
        lines.append(_paint(score, BOLD, colour))
    return "\n".join(lines)
