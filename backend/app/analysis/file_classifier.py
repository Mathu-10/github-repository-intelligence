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
    "setup.py",
    "setup.cfg",
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


EXAMPLE_DIRECTORIES = {
    "example",
    "examples",
    "demo",
    "demos",
    "sample",
    "samples",
}


def classify_file(path: str) -> str:
    file_path = PurePosixPath(path)

    # Skip files inside hidden directories (e.g. .spin/, .github/)
    if any(part.startswith(".") for part in file_path.parts[:-1]):
        return "other"

    file_name = file_path.name
    file_name_lower = file_name.lower()

    path_parts_lower = {
        part.lower()
        for part in file_path.parts
    }

    if (
        path_parts_lower & {"test", "tests", "t", "testing", "fixture", "fixtures"}
        or file_name_lower.startswith("test_")
        or file_name_lower.endswith("_test.py")
        or file_name_lower.endswith(".test.js")
        or file_name_lower.endswith(".test.ts")
    ):
        return "test"

    if (
        path_parts_lower
        & EXAMPLE_DIRECTORIES
        or path_parts_lower & {"bench", "benchmark", "benchmarks"}
        or file_name_lower.startswith("bench")
        or file_name_lower.startswith("benchmark")
    ):
        return "example"

    if any(
        part in {"docs", "doc", "documentation", "docs_src", "examples", "example", "tutorials", "tutorial", "website", "web", "playground", "playgrounds"}
        or part.startswith("docs_")
        or part.startswith("docs-")
        for part in path_parts_lower
    ):
        return "documentation"

    is_dependency = (
        file_name in DEPENDENCY_FILES
        or (file_path.parent.name.lower() == "requirements" and file_path.suffix.lower() == ".txt")
    )
    if is_dependency:
        return "dependency"

    if file_name_lower in DOCUMENTATION_FILES:
        return "documentation"

    if (
        file_name_lower in CONFIG_FILES
        or "config" in file_name_lower
        or file_name_lower in {"gruntfile.js", "gulpfile.js"}
    ):
        return "configuration"

    if any(
        part in {"release", "releases", "tool", "tools", "tooling", "task", "tasks", "scripts", "script"}
        for part in path_parts_lower
    ):
        return "other"

    if (
        file_path.suffix.lower()
        in SOURCE_EXTENSIONS
    ):
        return "source_code"

    return "other"