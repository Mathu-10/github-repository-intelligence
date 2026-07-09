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


def detect_entry_points(files: list[dict]) -> list[dict]:
    entry_points = []

    for file in files:
        path = file["path"]
        file_name = PurePosixPath(path).name.lower()
        content = file.get("content", "")

        reasons = []
        confidence_score = 0

        if file_name in ENTRY_POINT_NAMES:
            reasons.append("recognized_entry_point_filename")
            confidence_score += 50

        if 'if __name__ == "__main__"' in content:
            reasons.append("python_main_guard")
            confidence_score += 40

        if (
            "FastAPI(" in content
            or "Flask(" in content
            or "Django" in content
        ):
            reasons.append("web_application_initialization")
            confidence_score += 30

        if (
            "uvicorn.run(" in content
            or "app.run(" in content
        ):
            reasons.append("application_start_command")
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