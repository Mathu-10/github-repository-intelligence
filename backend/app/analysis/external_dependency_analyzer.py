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

        if file_path.stem != "__init__":
            internal_modules.add(
                file_path.stem
            )

        for part in file_path.parts[:-1]:
            if part not in {
                "src",
                "backend",
                "app",
                "tests",
                "test",
            }:
                internal_modules.add(part)

    return internal_modules


def find_external_dependencies(
    files: list[dict],
) -> list[dict]:

    standard_library = set(
        sys.stdlib_module_names
    )

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