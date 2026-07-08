from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.repository.github_client import (
    get_repository_metadata,
    get_repository_tree,
)
router = APIRouter()

class RepositoryRequest(BaseModel):
    repo_url: HttpUrl


@router.post("/analyze")

def analyze_repository(request: RepositoryRequest):
    repo_url = str(request.repo_url)

    if request.repo_url.host not in {"github.com", "www.github.com"}:
        raise HTTPException(
            status_code=400,
            detail="Only GitHub repository URLs are supported"
        )

    path_parts = [
        part for part in request.repo_url.path.split("/")
        if part
    ]

    if len(path_parts) != 2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    owner, repo = path_parts
    repo = repo.removesuffix(".git")

    metadata, error = get_repository_metadata(owner, repo)

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    tree, tree_error = get_repository_tree(
        owner,
        repo,
        metadata["default_branch"]
    )

    if tree_error:
        raise HTTPException(
            status_code=400,
            detail=tree_error
        )

    return {
    "status": "valid",
    "owner": owner,
    "repository": repo,
    "description": metadata.get("description"),
    "default_branch": metadata.get("default_branch"),
    "language": metadata.get("language"),
    "size_kb": metadata.get("size"),
    "stars": metadata.get("stargazers_count"),
    "forks": metadata.get("forks_count"),
    "files": tree
}