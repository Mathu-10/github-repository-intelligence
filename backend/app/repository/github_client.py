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

def get_repository_tree(owner: str, repo: str, branch: str):
    url = (
        f"{GITHUB_API_BASE_URL}/repos/"
        f"{owner}/{repo}/git/trees/{branch}?recursive=1"
    )

    try:
        response = requests.get(url, timeout=15)
    except requests.RequestException:
        return None, "Could not fetch repository structure"

    if response.status_code != 200:
        return None, f"Could not fetch repository tree: {response.status_code}"

    data = response.json()

    if data.get("truncated"):
        return None, "Repository tree is too large and was truncated"

    return data.get("tree", []), None