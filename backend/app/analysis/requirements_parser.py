import re


def normalize_package_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirements(content: str) -> list[dict]:
    dependencies = []

    for raw_line in content.splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith(("-r ", "--requirement ")):
            continue

        if line.startswith(("-e ", "--editable ")):
            continue

        if line.startswith(("-", "git+", "http://", "https://")):
            continue

        requirement = line.split(";", 1)[0].strip()

        match = re.match(
            r"^([A-Za-z0-9][A-Za-z0-9._-]*)"
            r"(?:\[([A-Za-z0-9,._-]+)\])?"
            r"\s*(.*)$",
            requirement,
        )

        if not match:
            continue

        package_name = match.group(1)
        extras = match.group(2)
        version_spec = match.group(3).strip()

        dependencies.append({
            "package": package_name,
            "normalized_name": normalize_package_name(
                package_name
            ),
            "extras": (
                extras.split(",")
                if extras
                else []
            ),
            "version_spec": version_spec or None,
        })

    return dependencies