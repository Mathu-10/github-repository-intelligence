import requests


GITHUB_API_BASE_URL = "https://api.github.com"


def get_repository_metadata(owner: str, repo: str):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None, "Could not connect to GitHub"

    if response.status_code == 404:
        return None, "Repository not found or is not public"

    if response.status_code != 200:
        return None, f"GitHub API error: {response.status_code}"

    return response.json(), None