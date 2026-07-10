import json
from pathlib import Path


def inspect_dataset(
    dataset_file: Path,
) -> dict:

    if not dataset_file.exists():
        return {
            "exists": False,
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "unique_repositories": 0,
            "duplicate_fingerprints": 0,
        }

    total_records = 0
    valid_records = 0
    invalid_records = 0

    repository_names = set()
    fingerprints = set()
    duplicate_fingerprints = 0

    with dataset_file.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            total_records += 1

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                invalid_records += 1
                continue

            valid_records += 1

            fingerprint = record.get("fingerprint")

            if fingerprint:
                if fingerprint in fingerprints:
                    duplicate_fingerprints += 1
                else:
                    fingerprints.add(fingerprint)

            repository_name = (
                record
                .get("input", {})
                .get("repository_summary", {})
                .get("repository_identity", {})
                .get("name")
            )

            if repository_name:
                repository_names.add(
                    repository_name
                )

    return {
        "exists": True,
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "unique_repositories": len(
            repository_names
        ),
        "duplicate_fingerprints": (
            duplicate_fingerprints
        ),
    }