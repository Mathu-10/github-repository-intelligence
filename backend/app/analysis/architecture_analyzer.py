from pathlib import PurePosixPath


def infer_repository_architecture(
    files: list[dict],
    external_dependencies: list[dict],
    entry_points: list[dict],
) -> dict:

    paths = [
        file["path"].lower()
        for file in files
    ]

    libraries = {
        dependency["library"].lower()
        for dependency in external_dependencies
    }

    directory_names = {
        part.lower()
        for path in paths
        for part in PurePosixPath(path).parts[:-1]
    }

    architecture_types = []
    evidence = []

    web_frameworks = {
        "fastapi",
        "flask",
        "django",
        "express",
    }

    detected_web_frameworks = sorted(
        libraries.intersection(web_frameworks)
    )

    if detected_web_frameworks:
        architecture_types.append("web_api_backend")
        evidence.append({
            "signal": "web_framework_detected",
            "values": detected_web_frameworks,
        })

    layer_directories = {
        "api",
        "repository",
        "analysis",
        "service",
        "services",
        "model",
        "models",
        "controller",
        "controllers",
    }

    detected_layers = sorted(
        directory_names.intersection(layer_directories)
    )

    if len(detected_layers) >= 2:
        architecture_types.append("layered_modular")
        evidence.append({
            "signal": "layer_directories_detected",
            "values": detected_layers,
        })

    if entry_points:
        evidence.append({
            "signal": "entry_points_detected",
            "values": [
                entry_point["path"]
                for entry_point in entry_points
            ],
        })

    if not architecture_types:
        architecture_types.append(
            "general_software_repository"
        )

    primary_architecture = architecture_types[0]

    return {
        "primary_architecture": primary_architecture,
        "architecture_types": architecture_types,
        "detected_layers": detected_layers,
        "evidence": evidence,
    }