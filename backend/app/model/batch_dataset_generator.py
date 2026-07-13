from app.services.repository_analysis_service import (
    analyze_repository_pipeline,
)


def analyze_repository_batch(
    repositories: list[dict],
) -> list[dict]:

    results = []

    for repository in repositories:
        owner = repository["owner"]
        repo = repository["repo"]

        result, error = analyze_repository_pipeline(
            owner,
            repo,
            save_training_record=False,
        )

        if error:
            results.append({
                "owner": owner,
                "repository": repo,
                "success": False,
                "error": error,
            })
            continue

        results.append({
            "owner": owner,
            "repository": repo,
            "success": True,
            "analysis": result,
        })

    return results