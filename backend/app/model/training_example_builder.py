import json
from app.analysis.file_classifier import classify_file


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

    # Determine reachable nodes from entry points via BFS
    reachable_nodes = set()
    if entry_point_paths:
        reachable_nodes.update(entry_point_paths)
        queue = list(entry_point_paths)

        adj = {}
        for edge in dependency_graph:
            src = edge["source"]
            tgt = edge["target"]
            adj.setdefault(src, []).append(tgt)

        while queue:
            curr = queue.pop(0)
            for neighbor in adj.get(curr, []):
                if neighbor not in reachable_nodes:
                    reachable_nodes.add(neighbor)
                    queue.append(neighbor)

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
                source in reachable_nodes
            ),
        })

    return dependency_paths


def determine_dependency_scope(declared_groups: list[str], used_by: list[str]) -> str:
    # 1. Determine scope from actual file usage first (evidence-based)
    used_categories = {classify_file(path) for path in used_by}

    if "source_code" in used_categories:
        return "runtime/source"

    if "test" in used_categories:
        return "test"

    if "documentation" in used_categories:
        return "documentation"

    if "example" in used_categories:
        return "example"

    # 2. Fallback to declared groups if no usage information is available
    for group in declared_groups:
        group_lower = group.lower()
        clean_group = (
            group_lower.split(":", 1)[1]
            if ":" in group_lower
            else group_lower
        )

        if clean_group == "runtime":
            return "runtime/source"
        elif any(t in clean_group for t in ["test", "testing", "tests", "pytest"]):
            return "test"
        elif any(d in clean_group for d in ["doc", "docs", "documentation"]):
            return "documentation"
        elif any(dv in clean_group for dv in ["dev", "development", "tool", "tooling", "lint", "linter", "format", "formatter", "build", "ci"]):
            return "configuration/other"

    return "runtime/source"


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

    # Categorize directly used dependencies
    runtime_deps = []
    test_deps = []
    docs_deps = []
    example_deps = []
    config_deps = []

    for dep in dependency_comparison.get("directly_used", []):
        name = dep["package_name"]
        groups = dep.get("declared_groups", [])
        used_by = dep.get("used_by", [])
        scope = determine_dependency_scope(groups, used_by)

        if scope == "runtime/source":
            runtime_deps.append(name)
        elif scope == "test":
            test_deps.append(name)
        elif scope == "documentation":
            docs_deps.append(name)
        elif scope == "example":
            example_deps.append(name)
        elif scope == "configuration/other":
            config_deps.append(name)

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

    if runtime_deps:
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

    explanation_parts = []
    if runtime_deps:
        explanation_parts.append(
            "Directly used runtime/source external packages are "
            + ", ".join(runtime_deps)
        )
    if docs_deps:
        explanation_parts.append(
            "Directly used documentation external packages are "
            + ", ".join(docs_deps)
        )
    if test_deps:
        explanation_parts.append(
            "Directly used test external packages are "
            + ", ".join(test_deps)
        )
    if example_deps:
        explanation_parts.append(
            "Directly used example external packages are "
            + ", ".join(example_deps)
        )
    if config_deps:
        explanation_parts.append(
            "Directly used configuration/other external packages are "
            + ", ".join(config_deps)
        )

    if not explanation_parts:
        dependency_explanation = (
            "Directly used external packages are none detected."
        )
    else:
        dependency_explanation = ". ".join(explanation_parts) + "."

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
        "dependency_explanation": dependency_explanation,
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