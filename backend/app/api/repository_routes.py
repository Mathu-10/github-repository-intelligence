from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.model.dataset_inspector import inspect_dataset
from app.model.dataset_writer import DATASET_FILE
from app.services.repository_analysis_service import (
    analyze_repository_pipeline,
)


router = APIRouter()


class RepositoryRequest(BaseModel):
    repo_url: HttpUrl
    save_training_record: bool = False


@router.post("/analyze")
def analyze_repository(
    request: RepositoryRequest,
):
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

    result, error = analyze_repository_pipeline(
        owner,
        repo,
        request.save_training_record,
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return result


@router.get("/dataset/stats")
def get_dataset_stats():
    return inspect_dataset(
        DATASET_FILE
    )