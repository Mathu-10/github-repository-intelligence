from pathlib import PurePosixPath


ENTRY_POINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "index.js",
    "index.ts",
    "server.js",
    "server.ts",
}


IMPORTANT_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "cargo.toml",
    "go.mod",
}


LOW_PRIORITY_NAMES = {
    ".gitignore",
    ".dockerignore",
    "license",
    "license.md",
    "changelog.md",
}


def calculate_file_score(file: dict) -> int:
    path = file["path"]
    file_path = PurePosixPath(path)
    file_name = file_path.name.lower()
    suffix = file_path.suffix.lower()

    score = 0

    if file_name in ENTRY_POINT_NAMES:
        score += 100

    if file_name in IMPORTANT_FILES:
        score += 80

    if suffix in {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".go",
        ".rs",
    }:
        score += 50

    if file_name.startswith("readme"):
        score += 40

    if "test" in {part.lower() for part in file_path.parts}:
        score -= 20

    if file_name in LOW_PRIORITY_NAMES:
        score -= 50

    file_size = file.get("size", 0)

    if 0 < file_size <= 100_000:
        score += 10

    return score


def rank_files(files: list[dict]) -> list[dict]:
    return sorted(
        files,
        key=lambda file: (
            calculate_file_score(file),
            -file.get("size", 0),
        ),
        reverse=True,
    )