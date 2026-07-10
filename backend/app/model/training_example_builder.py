import json


TRAINING_FORMAT_VERSION = "1.0"


def build_file_reason(file: dict) -> str:
    incoming_count = file.get("incoming_count", 0)
    outgoing_count = file.get("outgoing_count", 0)

    if incoming_count > 0 and outgoing_count > 0:
        return (
            f"Acts as an orchestration component with "
            f"{outgoing_count} outgoing internal dependencies "
            f"and is used by {incoming_count} other file(s)."
        )

    if incoming_count > 0:
        return (
            f"Provides shared functionality used by "
            f"{incoming_count} other file(s)."
        )

    if outgoing_count > 0:
        return (
            f"Coordinates {outgoing_count} internal "
            "dependency or dependencies."
        )

    return (
        "Ranked as structurally relevant by the "
        "repository analysis pipeline."
    )


def build_execution_flow(
    entry_points: list[dict],
    dependency_graph: list[dict],
) -> list[dict]:

    entry_point_paths = {
        entry_point["path"]
        for entry_point in entry_points
    }

    dependency_paths = []
    seen_relationships = set()

    for dependency in dependency_graph:
        source = dependency["source"]
        target = dependency["target"]

        relationship_key = (source, target)

        if relationship_key in seen_relationships:
            continue

        seen_relationships.add(
            relationship_key
        )

        dependency_paths.append({
            "source": source,
            "target": target,
            "relationship": "imports",
            "starts_from_entry_point": (
                source in entry_point_paths
            ),
        })

    return dependency_paths


def build_target_output(
    repository_summary: dict,
    entry_points: list[dict],
    structural_ranking: list[dict],
    dependency_comparison: dict,
    dependency_graph: list[dict],
) -> dict:

    identity = repository_summary.get(
        "repository_identity",
        {},
    )

    architecture = repository_summary.get(
        "architecture",
        {},
    )

    code_structure = repository_summary.get(
        "code_structure",
        {},
    )

    repository_name = (
        identity.get("name")
        or "the repository"
    )

    primary_architecture = (
        architecture.get("primary")
        or "general_software_repository"
    )

    important_files = [
        {
            "path": file["path"],
            "reason": build_file_reason(file),
        }
        for file in structural_ranking[:5]
    ]

    execution_flow = build_execution_flow(
        entry_points,
        dependency_graph,
    )

    directly_used = [
        dependency["package_name"]
        for dependency in dependency_comparison.get(
            "directly_used",
            [],
        )
    ]

    undeclared = [
        dependency["package_name"]
        for dependency in dependency_comparison.get(
            "imported_but_undeclared",
            [],
        )
    ]

    layers = architecture.get("layers", [])
    architecture_types = architecture.get("types", [])

    strengths = []

    if len(layers) >= 2:
        strengths.append(
            "Uses multiple detected layers to separate "
            "major repository responsibilities."
        )

    if directly_used:
        strengths.append(
            "Uses explicitly declared external packages "
            "for detected runtime functionality."
        )

    if entry_points and any(
    relationship.get("starts_from_entry_point")
        for relationship in execution_flow
    ):
        strengths.append(
            "Has a detectable internal dependency path beginning "
            "from an identified application entry point."
        )

    potential_improvements = []

    if undeclared:
        potential_improvements.append(
            "Declare imported packages that are missing "
            "from the dependency file: "
            + ", ".join(undeclared)
            + "."
        )

    if not potential_improvements:
        potential_improvements.append(
            "Add automated tests that validate repository "
            "analysis across different project structures."
        )

    return {
        "overview": (
            f"{repository_name} is analyzed as a "
            f"{primary_architecture} with "
            f"{code_structure.get('total_functions', 0)} "
            f"detected functions and "
            f"{code_structure.get('total_classes', 0)} "
            "detected classes."
        ),
        "purpose": (
            identity.get("description")
            or "No repository description was provided."
        ),
        "architecture_explanation": (
            "Detected architecture types are "
            + (
                ", ".join(architecture_types)
                if architecture_types
                else "not confidently identified"
            )
            + ". Detected layers are "
            + (
                ", ".join(layers)
                if layers
                else "none"
            )
            + "."
        ),
        "execution_flow": execution_flow,
        "important_files": important_files,
        "dependency_explanation": (
            "Directly used external packages are "
            + (
                ", ".join(directly_used)
                if directly_used
                else "none detected"
            )
            + "."
        ),
        "strengths": strengths,
        "potential_improvements": potential_improvements,
    }


def build_training_example(
    model_input: dict,
    target_output: dict,
) -> dict:

    return {
        "format_version": TRAINING_FORMAT_VERSION,
        "task": model_input["task"],
        "input": model_input,
        "output": target_output,
        "input_json": json.dumps(
            model_input,
            ensure_ascii=False,
            sort_keys=True,
        ),
        "output_json": json.dumps(
            target_output,
            ensure_ascii=False,
            sort_keys=True,
        ),
    }