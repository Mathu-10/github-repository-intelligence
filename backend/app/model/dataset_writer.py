import json
from pathlib import Path
from uuid import uuid4


DATASET_DIRECTORY = Path(
    "data/training"
)

DATASET_FILE = DATASET_DIRECTORY / "repository_examples.jsonl"


def validate_training_example(
    training_example: dict,
) -> tuple[bool, str | None]:

    required_keys = {
        "format_version",
        "task",
        "input",
        "output",
        "input_json",
        "output_json",
    }

    missing_keys = (
        required_keys - training_example.keys()
    )

    if missing_keys:
        return (
            False,
            "Missing training-example fields: "
            + ", ".join(sorted(missing_keys)),
        )

    required_output_fields = {
        "overview",
        "purpose",
        "architecture_explanation",
        "execution_flow",
        "important_files",
        "dependency_explanation",
        "strengths",
        "potential_improvements",
    }

    output = training_example.get("output", {})

    missing_output_fields = (
        required_output_fields - output.keys()
    )

    if missing_output_fields:
        return (
            False,
            "Missing output fields: "
            + ", ".join(
                sorted(missing_output_fields)
            ),
        )

    return True, None


def save_training_example(
    training_example: dict,
) -> tuple[dict | None, str | None]:

    is_valid, error = validate_training_example(
        training_example
    )

    if not is_valid:
        return None, error

    DATASET_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    record = {
        "record_id": str(uuid4()),
        **training_example,
    }

    try:
        with DATASET_FILE.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )
    except OSError as error:
        return None, (
            f"Could not save training example: {error}"
        )

    return {
        "saved": True,
        "record_id": record["record_id"],
        "dataset_path": str(DATASET_FILE),
    }, None