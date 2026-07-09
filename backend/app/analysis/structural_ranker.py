def calculate_structural_score(summary: dict) -> int:
    incoming_count = summary.get("incoming_count", 0)
    outgoing_count = summary.get("outgoing_count", 0)

    score = 0

    # Files used by many other files are structurally important.
    score += incoming_count * 30

    # Files coordinating many internal modules are also important.
    score += outgoing_count * 15

    return score


def rank_structurally_important_files(
    dependency_summary: list[dict],
) -> list[dict]:

    ranked_files = []

    for summary in dependency_summary:
        ranked_files.append({
            "path": summary["path"],
            "structural_score": calculate_structural_score(
                summary
            ),
            "incoming_count": summary["incoming_count"],
            "outgoing_count": summary["outgoing_count"],
            "depends_on": summary["depends_on"],
            "depended_on_by": summary["depended_on_by"],
        })

    return sorted(
        ranked_files,
        key=lambda file: (
            file["structural_score"],
            file["incoming_count"],
            file["outgoing_count"],
        ),
        reverse=True,
    )