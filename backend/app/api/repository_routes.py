from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

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

    return {
        "status": "valid",
        "owner": owner,
        "repository": repo,
        "repo_url": repo_url
    }