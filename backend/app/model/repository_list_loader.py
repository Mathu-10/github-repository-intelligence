import json
from pathlib import Path


REPOSITORY_LIST_FILE = Path(
    "data/repositories/curated_repositories.json"
)


def load_enabled_repositories() -> tuple[list[dict], str | None]:
    if not REPOSITORY_LIST_FILE.exists():
        return [], (
            f"Repository list not found: "
            f"{REPOSITORY_LIST_FILE}"
        )

    try:
        with REPOSITORY_LIST_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        return [], str(error)

    repositories = data.get("repositories")

    if not isinstance(repositories, list):
        return [], (
            "Invalid repository list: "
            "'repositories' must be a list"
        )

    enabled_repositories = [
        repository
        for repository in repositories
        if isinstance(repository, dict)
        and repository.get("enabled") is True
        and repository.get("url")
    ]

    return enabled_repositories, None