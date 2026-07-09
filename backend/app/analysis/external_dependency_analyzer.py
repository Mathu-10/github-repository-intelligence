import sys


def extract_root_module(import_name: str) -> str:
    return import_name.split(".")[0]


def find_external_dependencies(files: list[dict]) -> list[dict]:
    standard_library = set(sys.stdlib_module_names)
    dependency_usage = {}

    for file in files:
        analysis = file.get("analysis", {})

        if not analysis.get("success"):
            continue

        for import_name in analysis.get("imports", []):
            root_module = extract_root_module(import_name)

            if root_module in standard_library:
                continue

            if root_module == "app":
                continue

            if root_module not in dependency_usage:
                dependency_usage[root_module] = set()

            dependency_usage[root_module].add(file["path"])

    return [
        {
            "library": library,
            "used_by": sorted(paths),
            "usage_count": len(paths),
        }
        for library, paths in sorted(dependency_usage.items())
    ]