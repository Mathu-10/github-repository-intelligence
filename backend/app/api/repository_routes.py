from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.analysis.file_filter import filter_repository_tree
from app.repository.github_client import (
    get_repository_metadata,
    get_repository_tree,
)
from app.model.dataset_inspector import (
    inspect_dataset,
)
from app.model.dataset_writer import (
    DATASET_FILE,
    save_training_example,
)
from app.model.training_quality import (
    evaluate_training_example,
)
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
from app.model.model_schema import (
    build_model_input,
    build_model_output_template,
)
from app.analysis.entry_point_detector import (
    detect_entry_points,
)
from app.analysis.file_ranker import rank_files
from app.analysis.dependency_comparator import (
    compare_dependencies,
)
from app.analysis.requirements_parser import (
    parse_requirements,
)
from app.analysis.dependency_summary import (
    build_dependency_summary,
)
from app.repository.content_fetcher import (
    fetch_repository_contents,
)
from app.analysis.file_classifier import classify_file
from app.analysis.python_parser import parse_python_file
from app.analysis.dependency_analyzer import (
    build_python_dependency_graph,
)


router = APIRouter()


class RepositoryRequest(BaseModel):
    repo_url: HttpUrl
    save_training_record: bool = False


@router.post("/analyze")
def analyze_repository(
    request: RepositoryRequest,
):
    repo_url = str(request.repo_url)

    if request.repo_url.host not in {
        "github.com",
        "www.github.com",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only GitHub repository URLs "
                "are supported"
            ),
        )

    path_parts = [
        part
        for part in request.repo_url.path.split("/")
        if part
    ]

    if len(path_parts) != 2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL",
        )

    owner, repo = path_parts
    repo = repo.removesuffix(".git")

    metadata, error = get_repository_metadata(
        owner,
        repo,
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    tree, tree_error = get_repository_tree(
        owner,
        repo,
        metadata["default_branch"],
    )

    if tree_error:
        raise HTTPException(
            status_code=400,
            detail=tree_error,
        )

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

    dependency_graph = (
        build_python_dependency_graph(
            repository_contents
        )
    )

    dependency_summary = build_dependency_summary(
        repository_contents,
        dependency_graph,
    )

    structural_ranking = (
        rank_structurally_important_files(
            dependency_summary
        )
    )

    external_dependencies = (
        find_external_dependencies(
            repository_contents
        )
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
        if file["path"].lower().endswith(
            "requirements.txt"
        ):
            declared_dependencies.extend(
                parse_requirements(
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
        dependency_graph,
        repository_contents,
    )

    model_output_template = (
        build_model_output_template()
    )

    target_output = build_target_output(
        repository_summary,
        entry_points,
        structural_ranking,
        dependency_comparison,
        dependency_graph,
    )

    training_example = build_training_example(
        model_input,
        target_output,
    )

    training_quality = evaluate_training_example(
        training_example
    )

    dataset_save_result = None
    save_error = None

    if request.save_training_record:
        if not training_quality["passed"]:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": (
                        "Training example failed "
                        "the quality gate"
                    ),
                    "quality": training_quality,
                },
            )

        dataset_save_result, save_error = (
            save_training_example(
                training_example
            )
        )

        if save_error:
            raise HTTPException(
                status_code=500,
                detail=save_error,
            )

    return {
        "status": "valid",
        "repository": metadata.get("name"),

        # Temporarily hidden from Swagger response
        # "files": filtered_files,
        # "repository_contents": repository_contents,
        # "dependency_graph": dependency_graph,
        # "dependency_summary": dependency_summary,
        # "external_dependencies": external_dependencies,
        # "declared_dependencies": declared_dependencies,
        # "dependency_comparison": dependency_comparison,
        # "structural_ranking": structural_ranking,
        # "entry_points": entry_points,
        # "architecture": architecture,
        # "model_input": model_input,
        # "model_output_template": model_output_template,
        # "training_example": training_example,

        "repository_summary": repository_summary,
        "target_output": target_output,
        "dataset_save_result": dataset_save_result,
        "training_quality": training_quality,
    }


@router.get("/dataset/stats")
def get_dataset_stats():
    return inspect_dataset(
        DATASET_FILE
    )