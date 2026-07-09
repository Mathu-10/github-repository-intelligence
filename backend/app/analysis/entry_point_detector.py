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
    "index.js",
    "index.ts",
    "server.js",
    "server.ts",
}


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

        reasons = []
        confidence_score = 0

        if file_name in ENTRY_POINT_NAMES:
            reasons.append(
                "recognized_entry_point_filename"
            )
            confidence_score += 50

        if file_path.suffix.lower() == ".py":
            signals = get_python_signals(content)

            if signals["main_guard"]:
                reasons.append("python_main_guard")
                confidence_score += 40

            if signals["web_application_initialization"]:
                reasons.append(
                    "web_application_initialization"
                )
                confidence_score += 30

            if signals["application_start_command"]:
                reasons.append(
                    "application_start_command"
                )
                confidence_score += 30

        if reasons:
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