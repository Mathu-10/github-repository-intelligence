from pathlib import PurePosixPath
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
    fetched_paths = set()
    total_size = 0

    def add_file(file):
        nonlocal total_size
        file_path = file["path"]
        
        # Standardize path string
        file_path = file_path.replace("\\", "/")
        
        if file_path in fetched_paths:
            return False
            
        file_size = file.get("size", 0)
        if file_size > MAX_FILE_SIZE:
            return False
            
        if len(fetched_files) >= MAX_FILES:
            return False
            
        if total_size + file_size > MAX_TOTAL_SIZE:
            return False

        content, error = get_file_content(
            owner,
            repo,
            file["path"],
        )

        if error:
            return False

        fetched_files.append({
            "path": file["path"],
            "size": file_size,
            "content": content,
        })
        fetched_paths.add(file_path)
        total_size += file_size
        return True

    # 1. Reserve and fetch relevant dependency manifests first
    MANIFEST_NAMES = {
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "pipfile",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "cargo.toml",
        "go.mod",
    }
    
    for file in files:
        file_path = PurePosixPath(file["path"])
        is_manifest = (
            (len(file_path.parts) <= 2 and file_path.name.lower() in MANIFEST_NAMES)
            or (file_path.parent.name.lower() == "requirements" and file_path.suffix.lower() == ".txt")
        )
        if is_manifest:
            add_file(file)

    # 2. Identify the logical package root of all production source files
    from app.analysis.file_classifier import classify_file

    EXCLUDED_FOLDERS = {
        "docs", "doc", "examples", "example", "tests", "test", "t", "testing",
        "scripts", "script", "config", "configuration", "generated",
        "release", "releases", "tool", "tools", "tooling", "task", "tasks",
        "requirements", "web", "website", "playground", "playgrounds", "fixture", "fixtures"
    }
    source_paths = []
    for file in files:
        path = file["path"].replace("\\", "/")
        if classify_file(path) == "source_code":
            source_paths.append(PurePosixPath(path).parent)

    if not source_paths:
        package_root = PurePosixPath("")
    else:
        common = source_paths[0]
        for p in source_paths[1:]:
            common_parts = []
            for c_part, p_part in zip(common.parts, p.parts):
                if c_part == p_part:
                    common_parts.append(c_part)
                else:
                    break
            common = PurePosixPath(*common_parts)
        package_root = common

    # Group remaining files by component relative to package_root
    component_groups = {}
    remaining_files = []

    for file in files:
        file_path_str = file["path"].replace("\\", "/")
        if file_path_str in fetched_paths:
            continue
            
        file_path = PurePosixPath(file_path_str)
        
        # Determine if it belongs to a component relative to package_root
        component = None
        if classify_file(file_path_str) == "source_code":
            try:
                relative = file_path.relative_to(package_root)
                parts = relative.parts
                if len(parts) > 1:
                    component = parts[0]
            except ValueError:
                # Fallback to absolute segment if outside package_root
                parts = file_path.parts
                if len(parts) > 1:
                    component = parts[0]

        if component:
            if component not in component_groups:
                component_groups[component] = []
            component_groups[component].append(file)
        else:
            remaining_files.append(file)

    # 3. Interleaved component selection (round-robin)
    # Filter out empty components and sort active components keys to keep it deterministic
    active_components = sorted([
        comp for comp in component_groups.keys()
        if len(component_groups[comp]) > 0
    ])

    # Round-robin should only be applied when multiple logical production components exist.
    if len(active_components) > 1:
        indices = {comp: 0 for comp in active_components}
        
        while active_components and len(fetched_files) < MAX_FILES:
            to_remove = []
            for comp in active_components:
                idx = indices[comp]
                group_files = component_groups[comp]
                
                # Find the next file that can be fetched successfully
                while idx < len(group_files):
                    file = group_files[idx]
                    idx += 1
                    indices[comp] = idx
                    if add_file(file):
                        break
                
                if idx >= len(group_files):
                    to_remove.append(comp)
                    
                if len(fetched_files) >= MAX_FILES:
                    break
                    
            for comp in to_remove:
                if comp in active_components:
                    active_components.remove(comp)
                    
        # 4. Fill remaining budget slots from remaining files
        for file in remaining_files:
            if len(fetched_files) >= MAX_FILES:
                break
            add_file(file)
    else:
        # Fallback to linear fetch when single component is found, preserving existing ranking behavior
        for file in files:
            file_path_str = file["path"].replace("\\", "/")
            if file_path_str in fetched_paths:
                continue
            if len(fetched_files) >= MAX_FILES:
                break
            add_file(file)

    return fetched_files