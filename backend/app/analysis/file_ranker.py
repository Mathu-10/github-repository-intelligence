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


# A small curated set of common production-module filenames observed across multiple validated Python repositories.
COMMON_ARCHITECTURAL_FILENAMES = {
    "main.py",
    "core.py",
    "base.py",
    "engine.py",
    "console.py",
    "cli.py",
    "models.py",
    "types.py",
    "api.py",
    "server.py",
    "client.py",
}


def calculate_file_score(file: dict) -> int:
    path = file["path"]
    file_path = PurePosixPath(path)
    file_name = file_path.name.lower()
    suffix = file_path.suffix.lower()

    path_parts = {
        part.lower()
        for part in file_path.parts
    }

    score = 0

    # Core source directories should be fetched first
    if "src" in path_parts:
        score += 100

    # Application entry points
    if file_name in ENTRY_POINT_NAMES:
        score += 100

    # Dependency and project metadata
    is_manifest = (
        file_name in IMPORTANT_FILES
        or (file_path.parent.name.lower() == "requirements" and suffix == ".txt")
    )
    if is_manifest:
        score += 80

    # Source code
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

    # Architectural filename bonus for Python source files
    if suffix == ".py" and file_name in COMMON_ARCHITECTURAL_FILENAMES:
        # Do not apply to tests, docs, examples, tooling, scripts, or release files
        is_excluded_from_bonus = (
            path_parts & {
                "example", "examples", "demo", "demos", "sample", "samples",
                "doc", "docs", "docs_src", "documentation", "tutorial", "tutorials", "website",
                "test", "tests", "t", "testing", "script", "scripts", "release", "releases", "tool", "tools", "tooling", "task", "tasks"
            }
            or any(p.startswith("docs_") or p.startswith("docs-") for p in path_parts)
        )
        if not is_excluded_from_bonus:
            score += 15

    # README files
    if file_name.startswith("readme"):
        score += 40

    # Examples and documentation should not consume the core analysis budget
    if path_parts & {
        "example",
        "examples",
        "demo",
        "demos",
        "sample",
        "samples",
        "doc",
        "docs",
        "docs_src",
        "documentation",
        "tutorial",
        "tutorials",
        "website",
    } or any(p.startswith("docs_") or p.startswith("docs-") for p in path_parts):
        score -= 150

    # Tests are useful, but lower priority than core source
    if path_parts & {
        "test",
        "tests",
        "t",
        "testing",
    }:
        score -= 150

    # Scripts/tooling files are not part of runtime source code
    if path_parts & {
        "script",
        "scripts",
    }:
        score -= 80

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