from app.model.batch_dataset_generator import (
    analyze_repository_batch,
)


repositories = [
    {
        "owner": "pallets",
        "repo": "markupsafe",
    },
]


results = analyze_repository_batch(
    repositories
)

import json

print(
    json.dumps(
        results,
        indent=2,
    )
)