from pathlib import PurePosixPath


IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    "target",
}


IGNORED_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
}


IGNORED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".exe",
    ".dll",
    ".so",
    ".class",
    ".pyc",
    ".woff",
    ".woff2",
    ".ttf",
}


def should_analyze_file(path: str) -> bool:
    file_path = PurePosixPath(path)

    if any(part in IGNORED_DIRECTORIES for part in file_path.parts):
        return False

    if file_path.name in IGNORED_FILES:
        return False

    if file_path.suffix.lower() in IGNORED_EXTENSIONS:
        return False

    return True


def filter_repository_tree(tree: list[dict]) -> list[dict]:
    return [
        item
        for item in tree
        if item.get("type") == "blob"
        and should_analyze_file(item.get("path", ""))
    ]