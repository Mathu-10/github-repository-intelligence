import sys
from pathlib import PurePosixPath


def extract_root_module(
    import_name: str,
) -> str:
    return import_name.split(".")[0]


def find_internal_module_names(
    files: list[dict],
) -> set[str]:

    internal_modules = set()

    for file in files:
        path = file.get("path", "")

        if not path.lower().endswith(".py"):
            continue

        file_path = PurePosixPath(path)
        parts = file_path.parts

        # If the file is at the root, its stem is the module root
        if len(parts) == 1:
            if file_path.stem != "__init__":
                internal_modules.add(file_path.stem)
            continue

        # Find the top-level package/module root
        first_part = parts[0]
        if first_part in {"src", "backend"} and len(parts) > 2:
            import_root = parts[1]
        else:
            import_root = parts[0]

        # Ensure we don't treat tests, test, docs, example etc. as package roots
        if import_root not in {
            "tests", "test", "docs", "doc", "examples", "example",
            "scripts", "script", "config", "configuration", "generated"
        }:
            internal_modules.add(import_root)

        # Also add individual file stems for files directly under root or src/backend
        if len(parts) == 2:
            if file_path.stem != "__init__":
                internal_modules.add(file_path.stem)
        elif len(parts) == 3 and parts[0] in {"src", "backend"}:
            if file_path.stem != "__init__":
                internal_modules.add(file_path.stem)

    return internal_modules


def find_external_dependencies(
    files: list[dict],
) -> list[dict]:

    # Version-aware standard library modules list. We use sys.stdlib_module_names as
    # the base, and augment it with standard library modules introduced in newer Python
    # versions (such as annotationlib in Python 3.14) to support analyzing codebases
    # targeting newer Python releases than the running interpreter.
    standard_library = set(sys.stdlib_module_names)
    if "annotationlib" not in standard_library:
        standard_library.add("annotationlib")

    internal_modules = (
        find_internal_module_names(files)
    )

    dependency_usage = {}

    for file in files:
        analysis = file.get("analysis", {})

        if not analysis.get("success"):
            continue

        for import_name in analysis.get(
            "imports",
            [],
        ):
            if import_name.startswith("."):
                continue

            root_module = extract_root_module(
                import_name
            )

            if root_module in standard_library:
                continue

            if root_module in internal_modules:
                continue

            if root_module not in dependency_usage:
                dependency_usage[root_module] = set()

            dependency_usage[root_module].add(
                file["path"]
            )

    return [
        {
            "library": library,
            "used_by": sorted(paths),
            "usage_count": len(paths),
        }
        for library, paths
        in sorted(dependency_usage.items())
    ]