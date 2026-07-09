from pathlib import PurePosixPath


DEPENDENCY_FILES = {
    "requirements.txt",
    "package.json",
    "pyproject.toml",
    "Pipfile",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Cargo.toml",
    "go.mod",
}


DOCUMENTATION_FILES = {
    "readme.md",
    "readme.rst",
    "readme.txt",
    "contributing.md",
    "changelog.md",
}


CONFIG_FILES = {
    ".env.example",
    ".gitignore",
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "tsconfig.json",
    "vite.config.js",
    "vite.config.ts",
}


SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
}


def classify_file(path: str) -> str:
    file_path = PurePosixPath(path)
    file_name = file_path.name
    file_name_lower = file_name.lower()
    path_parts_lower = {part.lower() for part in file_path.parts}

    if (
        "test" in path_parts_lower
        or "tests" in path_parts_lower
        or file_name_lower.startswith("test_")
        or file_name_lower.endswith("_test.py")
        or file_name_lower.endswith(".test.js")
        or file_name_lower.endswith(".test.ts")
    ):
        return "test"

    if file_name in DEPENDENCY_FILES:
        return "dependency"

    if file_name_lower in DOCUMENTATION_FILES:
        return "documentation"

    if file_name_lower in {name.lower() for name in CONFIG_FILES}:
        return "configuration"

    if file_path.suffix.lower() in SOURCE_EXTENSIONS:
        return "source_code"

    return "other"