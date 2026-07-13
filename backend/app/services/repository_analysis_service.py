from app.analysis.file_filter import filter_repository_tree
from app.repository.github_client import (
    get_repository_metadata,
    get_repository_tree,
)
from app.analysis.pyproject_parser import parse_pyproject
from app.model.dataset_writer import save_training_example
from app.model.training_quality import evaluate_training_example
from app.model.training_example_builder import (
    build_target_output,
    build_training_example,
)
from app.analysis.external_dependency_analyzer import (
    find_external_dependencies,
)
from app.analysis.structural_ranker import (
    rank_structurally_important_files,
)
from app.analysis.architecture_analyzer import (
    infer_repository_architecture,
)
from app.analysis.repository_summarizer import (
    build_repository_summary,
)
from app.model.model_schema import build_model_input
from app.analysis.entry_point_detector import detect_entry_points
from app.analysis.file_ranker import rank_files
from app.analysis.dependency_comparator import compare_dependencies
from app.analysis.requirements_parser import parse_requirements
from app.analysis.dependency_summary import build_dependency_summary
from app.repository.content_fetcher import fetch_repository_contents
from app.analysis.file_classifier import classify_file
from app.analysis.python_parser import parse_python_file
from app.analysis.dependency_analyzer import (
    build_python_dependency_graph,
)


def analyze_repository_pipeline(
    owner: str,
    repo: str,
    save_training_record: bool = False,
) -> tuple[dict | None, str | None]:

    metadata, error = get_repository_metadata(
        owner,
        repo,
    )

    if error:
        return None, error

    tree, tree_error = get_repository_tree(
        owner,
        repo,
        metadata["default_branch"],
    )

    if tree_error:
        return None, tree_error

    filtered_files = filter_repository_tree(tree)
    ranked_files = rank_files(filtered_files)

    repository_contents = fetch_repository_contents(
        owner,
        repo,
        ranked_files,
    )

    for file in repository_contents:
        file["category"] = classify_file(
            file["path"]
        )

        if (
            file["category"] == "source_code"
            and file["path"].lower().endswith(".py")
        ):
            file["analysis"] = parse_python_file(
                file["content"]
            )

    dependency_graph = build_python_dependency_graph(
        repository_contents
    )

    primary_analysis_paths = {
        file["path"]
        for file in repository_contents
        if file.get("category") not in {
            "example",
            "test",
        }
    }

    primary_dependency_graph = [
        dependency
        for dependency in dependency_graph
        if (
            dependency["source"] in primary_analysis_paths
            and dependency["target"] in primary_analysis_paths
        )
    ]

    dependency_summary = build_dependency_summary(
        repository_contents,
        primary_dependency_graph,
    )

    structural_ranking = rank_structurally_important_files(
        dependency_summary
    )

    external_dependencies = find_external_dependencies(
        repository_contents
    )

    entry_points = detect_entry_points(
        repository_contents
    )

    architecture = infer_repository_architecture(
        repository_contents,
        external_dependencies,
        entry_points,
    )

    declared_dependencies = []

    for file in repository_contents:
        lower_path = file["path"].lower()

        parts = [part.lower() for part in file["path"].replace("\\", "/").split("/")]
        # Requirements directory text files must be directly inside a 'requirements' folder (parent index is parts[-2])
        is_requirements_file = (
            lower_path.endswith("requirements.txt")
            or (len(parts) >= 2 and parts[-2] == "requirements" and lower_path.endswith(".txt"))
        )

        if is_requirements_file:
            declared_dependencies.extend(
                parse_requirements(
                    file["content"]
                )
            )

        elif lower_path.endswith("pyproject.toml"):
            declared_dependencies.extend(
                parse_pyproject(
                    file["content"]
                )
            )

    dependency_comparison = compare_dependencies(
        external_dependencies,
        declared_dependencies,
    )

    repository_summary = build_repository_summary(
        metadata,
        repository_contents,
        architecture,
        entry_points,
        structural_ranking,
        external_dependencies,
        dependency_comparison,
    )

    model_input = build_model_input(
        repository_summary,
        structural_ranking,
        primary_dependency_graph,
        repository_contents,
    )

    target_output = build_target_output(
        repository_summary,
        entry_points,
        structural_ranking,
        dependency_comparison,
        primary_dependency_graph,
    )

    training_example = build_training_example(
        model_input,
        target_output,
    )

    training_quality = evaluate_training_example(
        training_example
    )

    dataset_save_result = None

    if save_training_record:
        if not training_quality["passed"]:
            return None, (
                "Training example failed the quality gate"
            )

        dataset_save_result, save_error = save_training_example(
            training_example
        )

        if save_error:
            return None, save_error

    result = {
        "status": "valid",
        "repository": metadata.get("name"),
        "repository_summary": repository_summary,
        "target_output": target_output,
        "dataset_save_result": dataset_save_result,
        "training_quality": training_quality,
    }

    return result, None