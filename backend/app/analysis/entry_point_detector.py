import ast
from pathlib import PurePosixPath


ENTRY_POINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "run.py",
    "wsgi.py",
    "asgi.py",
    "__main__.py",
    "index.js",
    "index.ts",
    "server.js",
    "server.ts",
}


BLOCKED_RUN_CALLERS = {
    "anyio",
    "from_thread",
    "executor",
    "runner",
    "task",
    "thread",
    "future",
    "callback",
    "self",
    "loop",
    "asyncio",
    "conn",
    "connection",
    "db",
    "cursor",
    "session",
    "client",
    "socket",
}


def get_attribute_path(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        prefix = get_attribute_path(node.value)
        if prefix:
            return f"{prefix}.{node.attr}"
    return None


def get_python_signals(content: str) -> dict:
    signals = {
        "main_guard": False,
        "web_application_initialization": False,
        "application_start_command": False,
    }

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return signals

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = node.test

            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):
                signals["main_guard"] = True

        if isinstance(node, ast.Call):
            function = node.func

            if isinstance(function, ast.Name):
                if function.id in {"FastAPI", "Flask"}:
                    signals[
                        "web_application_initialization"
                    ] = True

            elif isinstance(function, ast.Attribute):
                if function.attr == "run":
                    caller_path = get_attribute_path(function.value)
                    if caller_path:
                        path_parts = {p.lower() for p in caller_path.split(".")}
                        if not (path_parts & BLOCKED_RUN_CALLERS):
                            signals[
                                "application_start_command"
                            ] = True

    return signals


def detect_entry_points(files: list[dict]) -> list[dict]:
    entry_points = []

    for file in files:
        path = file["path"]
        file_path = PurePosixPath(path)
        file_name = file_path.name.lower()
        content = file.get("content", "")

        # Skip package __init__.py files
        if file_name == "__init__.py":
            continue

        path_parts_lower = {part.lower() for part in file_path.parts}

        # Skip generated OpenAPI client entry points
        if "client" in path_parts_lower and file_name in {"index.ts", "index.js", "index.tsx", "index.jsx"}:
            continue

        # Skip router aggregation modules
        if "api" in path_parts_lower and file_name in {"main.py", "app.py"}:
            continue

        # Skip files in documentation/example/test paths
        is_doc_or_test_or_example = False
        for part in path_parts_lower:
            if (
                part in {"tests", "test", "docs", "doc", "documentation", "docs_src", "examples", "example", "tutorials", "tutorial", "website"}
                or part.startswith("docs_")
                or part.startswith("docs-")
            ):
                is_doc_or_test_or_example = True
                break
        if is_doc_or_test_or_example:
            continue

        # Skip non-source-code files or files categorized as test/example
        category = file.get("category", "")
        if category in {"test", "example", "documentation", "dependency", "configuration"}:
            continue

        reasons = []
        confidence_score = 0
        is_ambiguous_web = file_name in {"wsgi.py", "asgi.py", "app.py", "main.py"}
        has_python_signal = False

        if file_path.suffix.lower() == ".py":
            signals = get_python_signals(content)
            has_python_signal = any(signals.values())

            if signals["main_guard"]:
                reasons.append("python_main_guard")
                confidence_score += 40

            if signals["web_application_initialization"]:
                reasons.append("web_application_initialization")
                confidence_score += 30

            if signals["application_start_command"]:
                reasons.append("application_start_command")
                confidence_score += 30

        if file_name in ENTRY_POINT_NAMES:
            # Ambiguous wsgi.py/asgi.py require at least one python signal to be considered
            if not is_ambiguous_web or has_python_signal:
                reasons.append("recognized_entry_point_filename")
                confidence_score += 50

        # Only classify as an entry point if it has sufficiently high evidence score (>= 50)
        # to distinguish from files that merely contain executable helper logic or library submodules.
        if reasons and confidence_score >= 50:
            entry_points.append({
                "path": path,
                "confidence_score": confidence_score,
                "reasons": reasons,
            })

    return sorted(
        entry_points,
        key=lambda item: item["confidence_score"],
        reverse=True,
    )