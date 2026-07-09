from pathlib import PurePosixPath


def get_module_variants(path: str) -> list[str]:
    file_path = PurePosixPath(path)

    if file_path.suffix != ".py":
        return []

    module_parts = list(file_path.with_suffix("").parts)

    if module_parts[-1] == "__init__":
        module_parts = module_parts[:-1]

    variants = []

    for index in range(len(module_parts)):
        variant = ".".join(module_parts[index:])

        if variant:
            variants.append(variant)

    return variants


def build_python_dependency_graph(files: list[dict]) -> list[dict]:
    python_files = [
        file
        for file in files
        if file.get("analysis", {}).get("success")
        and file["path"].lower().endswith(".py")
    ]

    module_to_path = {}

    for file in python_files:
        for module_name in get_module_variants(file["path"]):
            module_to_path[module_name] = file["path"]

    relationships = []
    seen_relationships = set()

    for file in python_files:
        source_path = file["path"]
        imports = file["analysis"].get("imports", [])

        for imported_module in imports:
            for module_name, target_path in module_to_path.items():
                if (
                    imported_module == module_name
                    or imported_module.startswith(module_name + ".")
                ):
                    if source_path == target_path:
                        continue

                    relationship_key = (
                        source_path,
                        target_path,
                        imported_module,
                    )

                    if relationship_key in seen_relationships:
                        continue

                    seen_relationships.add(relationship_key)

                    relationships.append({
                        "source": source_path,
                        "target": target_path,
                        "import": imported_module,
                    })

    return relationships