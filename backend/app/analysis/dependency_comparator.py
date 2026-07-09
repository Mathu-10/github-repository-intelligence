IMPORT_TO_PACKAGE_MAP = {
    "dotenv": "python-dotenv",
}


def compare_dependencies(
    external_dependencies: list[dict],
    declared_dependencies: list[dict],
) -> dict:

    declared_names = {
        dependency["normalized_name"]
        for dependency in declared_dependencies
    }

    directly_used = []
    imported_but_undeclared = []

    for dependency in external_dependencies:
        import_name = dependency["library"]

        package_name = IMPORT_TO_PACKAGE_MAP.get(
            import_name,
            import_name,
        )

        normalized_package = package_name.lower().replace(
            "_",
            "-",
        )

        result = {
            "import_name": import_name,
            "package_name": normalized_package,
            "used_by": dependency["used_by"],
            "usage_count": dependency["usage_count"],
        }

        if normalized_package in declared_names:
            directly_used.append(result)
        else:
            imported_but_undeclared.append(result)

    directly_used_packages = {
        dependency["package_name"]
        for dependency in directly_used
    }

    declared_not_directly_imported = [
        dependency
        for dependency in declared_dependencies
        if dependency["normalized_name"]
        not in directly_used_packages
    ]

    return {
        "directly_used": directly_used,
        "imported_but_undeclared": imported_but_undeclared,
        "declared_not_directly_imported": (
            declared_not_directly_imported
        ),
    }