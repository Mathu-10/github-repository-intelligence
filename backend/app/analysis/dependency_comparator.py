IMPORT_TO_PACKAGE_MAP = {
    "dotenv": "python-dotenv",
    "jwt": "PyJWT",
    "dateutil": "python-dateutil",
    "multipart": "python-multipart",
    "yaml": "pyyaml",
}


def normalize_package_name(
    name: str,
) -> str:
    return name.lower().replace(
        "_",
        "-",
    )


def compare_dependencies(
    external_dependencies: list[dict],
    declared_dependencies: list[dict],
) -> dict:

    declared_by_name = {}

    for dependency in declared_dependencies:
        normalized_name = dependency[
            "normalized_name"
        ]

        declared_by_name.setdefault(
            normalized_name,
            [],
        ).append(dependency)

    directly_used = []
    imported_but_undeclared = []

    for dependency in external_dependencies:
        import_name = dependency["library"]

        package_name = IMPORT_TO_PACKAGE_MAP.get(
            import_name,
            import_name,
        )

        normalized_package = (
            normalize_package_name(
                package_name
            )
        )

        declarations = declared_by_name.get(
            normalized_package,
            [],
        )

        result = {
            "import_name": import_name,
            "package_name": normalized_package,
            "used_by": dependency["used_by"],
            "usage_count": dependency["usage_count"],
            "declared_groups": sorted({
                declaration.get(
                    "group",
                    "runtime",
                )
                for declaration in declarations
            }),
        }

        if declarations:
            directly_used.append(result)
        else:
            imported_but_undeclared.append(
                result
            )

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
        "imported_but_undeclared": (
            imported_but_undeclared
        ),
        "declared_not_directly_imported": (
            declared_not_directly_imported
        ),
    }