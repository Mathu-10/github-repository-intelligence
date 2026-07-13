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
    valid_paths = {file["path"] for file in python_files}

    for file in python_files:
        for module_name in get_module_variants(file["path"]):
            module_to_path[module_name] = file["path"]

    relationships = []
    seen_relationships = set()

    for file in python_files:
        source_path = file["path"]
        imports = file["analysis"].get("imports", [])

        for imported_module in imports:
            if imported_module.startswith("."):
                # Count leading dots
                L = len(imported_module) - len(imported_module.lstrip("."))
                rest = imported_module.lstrip(".")

                # Resolve target base directory by going up L - 1 times from source's parent
                target_dir = PurePosixPath(source_path).parent
                for _ in range(L - 1):
                    target_dir = target_dir.parent

                rest_parts = rest.split(".") if rest else []

                resolved_path = None
                for k in range(len(rest_parts), 0, -1):
                    prefix = rest_parts[:k]

                    candidate_file_path = str(target_dir / "/".join(prefix)) + ".py"
                    candidate_init_path = str(target_dir / "/".join(prefix) / "__init__.py")

                    candidate_file_path = candidate_file_path.replace("\\", "/")
                    candidate_init_path = candidate_init_path.replace("\\", "/")

                    if candidate_file_path in valid_paths:
                        resolved_path = candidate_file_path
                        break
                    elif candidate_init_path in valid_paths:
                        resolved_path = candidate_init_path
                        break

                if resolved_path and source_path != resolved_path:
                    relationship_key = (
                        source_path,
                        resolved_path,
                        imported_module,
                    )
                    if relationship_key not in seen_relationships:
                        seen_relationships.add(relationship_key)
                        relationships.append({
                            "source": source_path,
                            "target": resolved_path,
                            "import": imported_module,
                        })
            else:
                target_path = None
                parts = imported_module.split(".")
                for k in range(len(parts), 0, -1):
                    candidate = ".".join(parts[:k])
                    if candidate in module_to_path:
                        target_path = module_to_path[candidate]
                        break

                if target_path and source_path != target_path:
                    relationship_key = (
                        source_path,
                        target_path,
                        imported_module,
                    )

                    if relationship_key not in seen_relationships:
                        seen_relationships.add(relationship_key)

                        relationships.append({
                            "source": source_path,
                            "target": target_path,
                            "import": imported_module,
                        })

    return relationships