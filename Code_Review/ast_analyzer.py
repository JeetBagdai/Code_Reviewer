import ast
import re


def _detect_language(code: str) -> str:
    if re.search(r'\bdef\b|\bimport\b|\bclass\b|\bprint\s*\(', code):
        return "Python"
    if re.search(r'\bfunction\b|\bconst\b|\blet\b|\bvar\b|\bconsolelog\b', code):
        return "JavaScript"
    if re.search(r'#include|int main|std::', code):
        return "C/C++"
    if re.search(r'\bpublic\s+class\b|\bSystem\.out\b', code):
        return "Java"
    return "Unknown"


class _ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.bugs = []
        self.quality_issues = []
        self.function_count = 0
        self.import_names = []
        self.used_names = set()
        self.has_main_guard = False
        self.max_function_lines = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        if lines > 40:
            self.bugs.append(f"Function '{node.name}' is too long ({lines} lines). Consider splitting it.")
        if self.max_function_lines < lines:
            self.max_function_lines = lines

        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                self.bugs.append(
                    f"Mutable default argument in '{node.name}' — use None as default and initialize inside."
                )

        if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant)):
            self.quality_issues.append(f"Function '{node.name}' is missing a docstring.")

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.bugs.append("Bare 'except:' clause found — catch specific exceptions to avoid masking errors.")
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.import_names.append(alias.asname or alias.name.split(".")[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name != "*":
                self.import_names.append(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_If(self, node):
        if (
            isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
        ):
            self.has_main_guard = True
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant)):
            self.quality_issues.append(f"Class '{node.name}' is missing a docstring.")
        self.generic_visit(node)


def _estimate_complexity(visitor: _ASTVisitor, code: str) -> dict:
    lines = code.strip().splitlines()
    loc = len([l for l in lines if l.strip() and not l.strip().startswith("#")])

    loops = sum(1 for line in lines if re.search(r'\bfor\b|\bwhile\b', line))
    nested_indicator = any(
        re.search(r'^\s{8,}(for|while)\b', line) for line in lines
    )

    if nested_indicator or loops >= 3:
        time_c = "O(n²)"
    elif loops >= 1:
        time_c = "O(n)"
    else:
        time_c = "O(1)"

    if re.search(r'\brecursi\w+\b', code, re.IGNORECASE) or visitor.max_function_lines > 30:
        space_c = "O(n)"
    else:
        space_c = "O(1)"

    return {"time": time_c, "space": space_c}


def _compute_score(bugs: list, quality_issues: list) -> int:
    score = 100
    score -= len(bugs) * 15
    score -= len(quality_issues) * 5
    return max(0, min(100, score))


def analyze(code: str) -> dict:
    language = _detect_language(code)
    bugs = []
    quality_issues = []
    complexity = {"time": "O(?)", "space": "O(?)"}

    if language == "Python":
        try:
            tree = ast.parse(code)
            visitor = _ASTVisitor()
            visitor.visit(tree)
            bugs = visitor.bugs
            quality_issues = visitor.quality_issues

            unused = [
                name for name in visitor.import_names
                if name not in visitor.used_names and name != "_"
            ]
            if unused:
                quality_issues.append(f"Potentially unused imports: {', '.join(unused)}")

            if visitor.function_count > 1 and not visitor.has_main_guard:
                quality_issues.append("Missing 'if __name__ == __main__:' guard for script-level code.")

            complexity = _estimate_complexity(visitor, code)
        except SyntaxError as e:
            bugs.append(f"Syntax error: {e.msg} at line {e.lineno}")
    else:
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            if re.search(r'TODO|FIXME|HACK|XXX', line):
                quality_issues.append(f"Line {i}: Found TODO/FIXME marker — unfinished work.")

    score = _compute_score(bugs, quality_issues)
    snippet = code.strip()[:120].replace("\n", " ") + ("..." if len(code) > 120 else "")

    return {
        "bugs": bugs,
        "quality_issues": quality_issues,
        "complexity": complexity,
        "score": score,
        "language": language,
        "snippet": snippet,
    }
