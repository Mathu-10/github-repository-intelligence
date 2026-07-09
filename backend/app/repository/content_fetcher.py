from app.repository.github_client import get_file_content


MAX_FILE_SIZE = 200_000       # 200 KB per file
MAX_FILES = 50                # temporary safety limit
MAX_TOTAL_SIZE = 2_000_000    # 2 MB per repository


def fetch_repository_contents(
    owner: str,
    repo: str,
    files: list[dict],
) -> list[dict]:

    fetched_files = []
    total_size = 0

    for file in files:
        file_size = file.get("size", 0)

        if file_size > MAX_FILE_SIZE:
            continue

        if len(fetched_files) >= MAX_FILES:
            break

        if total_size + file_size > MAX_TOTAL_SIZE:
            break

        content, error = get_file_content(
            owner,
            repo,
            file["path"],
        )

        if error:
            continue

        fetched_files.append({
            "path": file["path"],
            "size": file_size,
            "content": content,
        })

        total_size += file_size

    return fetched_files