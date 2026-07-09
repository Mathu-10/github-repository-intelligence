from collections import Counter


def build_repository_summary(
    metadata: dict,
    repository_contents: list[dict],
    architecture: dict,
    entry_points: list[dict],
    structural_ranking: list[dict],
    external_dependencies: list[dict],
    dependency_comparison: dict,
) -> dict:

    category_counts = Counter(
        file.get("category", "unknown")
        for file in repository_contents
    )

    language_counts = Counter()

    extension_to_language = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".go": "Go",
        ".rs": "Rust",
    }

    total_functions = 0
    total_classes = 0

    for file in repository_contents:
        path = file["path"].lower()

        for extension, language in extension_to_language.items():
            if path.endswith(extension):
                language_counts[language] += 1
                break

        analysis = file.get("analysis", {})

        if analysis.get("success"):
            total_functions += len(
                analysis.get("functions", [])
            )
            total_classes += len(
                analysis.get("classes", [])
            )

    important_files = [
        {
            "path": file["path"],
            "structural_score": file["structural_score"],
        }
        for file in structural_ranking[:5]
    ]

    direct_dependencies = [
        dependency["package_name"]
        for dependency in dependency_comparison.get(
            "directly_used",
            [],
        )
    ]

    undeclared_dependencies = [
        dependency["package_name"]
        for dependency in dependency_comparison.get(
            "imported_but_undeclared",
            [],
        )
    ]

    return {
        "repository_identity": {
            "name": metadata.get("name"),
            "description": metadata.get("description"),
            "primary_language": metadata.get("language"),
        },
        "architecture": {
            "primary": architecture.get(
                "primary_architecture"
            ),
            "types": architecture.get(
                "architecture_types",
                [],
            ),
            "layers": architecture.get(
                "detected_layers",
                [],
            ),
        },
        "entry_points": [
            entry_point["path"]
            for entry_point in entry_points
        ],
        "important_files": important_files,
        "languages_by_file_count": dict(language_counts),
        "file_categories": dict(category_counts),
        "code_structure": {
            "total_functions": total_functions,
            "total_classes": total_classes,
        },
        "dependencies": {
            "directly_used": direct_dependencies,
            "imported_but_undeclared": (
                undeclared_dependencies
            ),
            "external_library_count": len(
                external_dependencies
            ),
        },
    }