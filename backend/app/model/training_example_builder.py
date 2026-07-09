import json


TRAINING_FORMAT_VERSION = "1.0"


def build_target_output(
    repository_summary: dict,
    entry_points: list[dict],
    structural_ranking: list[dict],
    dependency_comparison: dict,
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
            "reason": (
                "Structurally important based on "
                "internal dependency relationships."
            ),
        }
        for file in structural_ranking[:5]
    ]

    execution_flow = [
        entry_point["path"]
        for entry_point in entry_points
    ]

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

    strengths = [
        "Uses a modular repository structure.",
        "Separates repository access from analysis logic.",
        "Builds explanations from verified static-analysis facts.",
    ]

    potential_improvements = []

    if undeclared:
        potential_improvements.append(
            "Declare imported packages that are missing "
            "from the dependency file."
        )

    if not potential_improvements:
        potential_improvements.append(
            "Add broader automated tests and evaluation "
            "for repository-analysis accuracy."
        )

    return {
        "overview": (
            f"{repository_name} is a "
            f"{primary_architecture} repository with "
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
            "The repository uses the detected architecture "
            f"types: {', '.join(architecture.get('types', []))}."
        ),
        "execution_flow": execution_flow,
        "important_files": important_files,
        "dependency_explanation": (
            "Directly used external packages: "
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