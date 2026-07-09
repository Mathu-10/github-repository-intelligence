from typing import Any


MODEL_SCHEMA_VERSION = "1.0"


def build_model_input(
    repository_summary: dict,
    structural_ranking: list[dict],
    dependency_graph: list[dict],
    repository_contents: list[dict],
) -> dict:

    files_by_path = {
        file["path"]: file
        for file in repository_contents
    }

    important_file_details = []

    for ranked_file in structural_ranking[:5]:
        path = ranked_file["path"]
        file = files_by_path.get(path)

        if not file:
            continue

        analysis = file.get("analysis", {})

        important_file_details.append({
            "path": path,
            "structural_score": ranked_file[
                "structural_score"
            ],
            "category": file.get("category"),
            "functions": [
                function["name"]
                for function in analysis.get(
                    "functions",
                    [],
                )
            ],
            "classes": [
                class_info["name"]
                for class_info in analysis.get(
                    "classes",
                    [],
                )
            ],
            "imports": analysis.get("imports", []),
        })

    return {
        "schema_version": MODEL_SCHEMA_VERSION,
        "task": "explain_repository",
        "repository_summary": repository_summary,
        "important_file_details": important_file_details,
        "internal_dependencies": dependency_graph,
    }


def build_model_output_template() -> dict[str, Any]:
    return {
        "overview": "",
        "purpose": "",
        "architecture_explanation": "",
        "execution_flow": [],
        "important_files": [],
        "dependency_explanation": "",
        "strengths": [],
        "potential_improvements": [],
    }