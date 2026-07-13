import re
import tomllib


def normalize_package_name(name: str) -> str:
    return re.sub(
        r"[-_.]+",
        "-",
        name,
    ).lower()


def build_dependency(
    package_name: str,
    version_spec: str | None = None,
    group: str = "runtime",
) -> dict:

    return {
        "package": package_name,
        "normalized_name": normalize_package_name(
            package_name
        ),
        "extras": [],
        "version_spec": version_spec,
        "group": group,
    }


def parse_dependency_string(
    dependency: str,
    group: str,
) -> dict | None:

    dependency = dependency.split(
        ";",
        1,
    )[0].strip()

    match = re.match(
        r"^([A-Za-z0-9][A-Za-z0-9._-]*)"
        r"(?:\[[^\]]+\])?"
        r"\s*(.*)$",
        dependency,
    )

    if not match:
        return None

    package_name = match.group(1)
    version_spec = (
        match.group(2).strip() or None
    )

    return build_dependency(
        package_name,
        version_spec,
        group,
    )


def parse_dependency_list(
    dependencies: list,
    group: str,
) -> list[dict]:

    parsed_dependencies = []

    for dependency in dependencies:
        if not isinstance(dependency, str):
            continue

        parsed = parse_dependency_string(
            dependency,
            group,
        )

        if parsed:
            parsed_dependencies.append(parsed)

    return parsed_dependencies


def parse_pyproject(
    content: str,
) -> list[dict]:

    try:
        data = tomllib.loads(content)
    except (
        tomllib.TOMLDecodeError,
        ValueError,
    ):
        return []

    dependencies = []

    project = data.get("project", {})

    dependencies.extend(
        parse_dependency_list(
            project.get("dependencies", []),
            "runtime",
        )
    )

    optional_dependencies = project.get(
        "optional-dependencies",
        {},
    )

    for group_name, group_dependencies in (
        optional_dependencies.items()
    ):
        dependencies.extend(
            parse_dependency_list(
                group_dependencies,
                f"optional:{group_name}",
            )
        )

    dependency_groups = data.get(
        "dependency-groups",
        {},
    )

    for group_name, group_dependencies in (
        dependency_groups.items()
    ):
        dependencies.extend(
            parse_dependency_list(
                group_dependencies,
                f"group:{group_name}",
            )
        )

    build_system = data.get("build-system", {})
    dependencies.extend(
        parse_dependency_list(
            build_system.get("requires", []),
            "build",
        )
    )

    return dependencies