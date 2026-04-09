"""
Style analyzer module.
Runs PEP 8 / pycodestyle checks for Python code.
For other languages, returns an empty list (external linters handle them).
"""


def analyze_style(code_string: str, language: str) -> list[dict]:
    """Return a list of style violation dicts for the given code.

    Each dict has keys: code, message, line, column.
    """
    if language != "Python":
        return []

    violations = []
    try:
        import pycodestyle

        lines = code_string.splitlines(True)
        # Ensure last line has a newline so pycodestyle is happy
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"

        checker = pycodestyle.Checker(
            "<stdin>",
            lines=lines,
            show_source=False,
            show_pep8=False,
            quiet=True,
        )
        checker.check_all()
        for line_number, offset, code, text, _ in checker.results:
            violations.append(
                {
                    "code": code,
                    "message": text,
                    "line": line_number,
                    "column": offset + 1,
                }
            )
    except ImportError:
        # pycodestyle is optional — skip silently
        pass
    except Exception:
        pass

    return violations
