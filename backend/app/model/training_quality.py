REQUIRED_OUTPUT_FIELDS = {
    "overview",
    "purpose",
    "architecture_explanation",
    "execution_flow",
    "important_files",
    "dependency_explanation",
    "strengths",
    "potential_improvements",
}


def evaluate_training_example(
    training_example: dict,
) -> dict:

    score = 0
    checks = []

    model_input = training_example.get("input", {})
    output = training_example.get("output", {})

    repository_summary = model_input.get(
        "repository_summary",
        {},
    )

    important_file_details = model_input.get(
        "important_file_details",
        [],
    )

    internal_dependencies = model_input.get(
        "internal_dependencies",
        [],
    )

    # 1. Repository summary: 20 points
    if repository_summary:
        score += 20
        checks.append({
            "check": "repository_summary_present",
            "passed": True,
            "points": 20,
        })
    else:
        checks.append({
            "check": "repository_summary_present",
            "passed": False,
            "points": 0,
        })

    # 2. Important file evidence: 20 points
    if important_file_details:
        score += 20
        checks.append({
            "check": "important_files_present",
            "passed": True,
            "points": 20,
        })
    else:
        checks.append({
            "check": "important_files_present",
            "passed": False,
            "points": 0,
        })

    # 3. Dependency evidence: 15 points
    if internal_dependencies:
        score += 15
        checks.append({
            "check": "dependency_evidence_present",
            "passed": True,
            "points": 15,
        })
    else:
        checks.append({
            "check": "dependency_evidence_present",
            "passed": False,
            "points": 0,
        })

    # 4. Complete output schema: 20 points
    missing_output_fields = (
        REQUIRED_OUTPUT_FIELDS - output.keys()
    )

    if not missing_output_fields:
        score += 20
        checks.append({
            "check": "output_schema_complete",
            "passed": True,
            "points": 20,
        })
    else:
        checks.append({
            "check": "output_schema_complete",
            "passed": False,
            "points": 0,
        })

    # 5. Non-empty explanatory text: 15 points
    text_fields = [
        output.get("overview", ""),
        output.get("purpose", ""),
        output.get(
            "architecture_explanation",
            "",
        ),
        output.get(
            "dependency_explanation",
            "",
        ),
    ]

    if all(
        isinstance(value, str) and value.strip()
        for value in text_fields
    ):
        score += 15
        checks.append({
            "check": "explanatory_text_present",
            "passed": True,
            "points": 15,
        })
    else:
        checks.append({
            "check": "explanatory_text_present",
            "passed": False,
            "points": 0,
        })

    # 6. Structured target lists: 10 points
    list_fields = [
        output.get("execution_flow"),
        output.get("important_files"),
        output.get("strengths"),
        output.get("potential_improvements"),
    ]

    if all(
        isinstance(value, list) and len(value) > 0
        for value in list_fields
    ):
        score += 10
        checks.append({
            "check": "structured_target_lists_present",
            "passed": True,
            "points": 10,
        })
    else:
        checks.append({
            "check": "structured_target_lists_present",
            "passed": False,
            "points": 0,
        })

    return {
        "score": score,
        "maximum_score": 100,
        "passed": score >= 70,
        "minimum_required_score": 70,
        "checks": checks,
    }