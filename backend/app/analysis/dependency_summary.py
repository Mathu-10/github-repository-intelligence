def build_dependency_summary(
    files: list[dict],
    relationships: list[dict],
) -> list[dict]:

    python_paths = [
        file["path"]
        for file in files
        if file.get("analysis", {}).get("success")
        and file["path"].lower().endswith(".py")
    ]

    summaries = {
        path: {
            "path": path,
            "depends_on": [],
            "depended_on_by": [],
            "outgoing_count": 0,
            "incoming_count": 0,
        }
        for path in python_paths
    }

    for relationship in relationships:
        source = relationship["source"]
        target = relationship["target"]

        if source not in summaries or target not in summaries:
            continue

        if target not in summaries[source]["depends_on"]:
            summaries[source]["depends_on"].append(target)

        if source not in summaries[target]["depended_on_by"]:
            summaries[target]["depended_on_by"].append(source)

    for summary in summaries.values():
        summary["outgoing_count"] = len(summary["depends_on"])
        summary["incoming_count"] = len(summary["depended_on_by"])

    return list(summaries.values())