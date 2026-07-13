from unittest.mock import patch
from app.repository.content_fetcher import fetch_repository_contents


@patch("app.repository.content_fetcher.get_file_content")
def test_single_component_repository(mock_get_content):
    mock_get_content.return_value = ("mock content", None)

    files = [
        {"path": "pyproject.toml", "size": 100},
        {"path": "src/a.py", "size": 100},
        {"path": "src/b.py", "size": 100},
        {"path": "src/c.py", "size": 100},
    ]

    fetched = fetch_repository_contents("owner", "repo", files)

    # Manifest is fetched first, followed by src/ in ranking order
    expected_order = [
        "pyproject.toml",
        "src/a.py",
        "src/b.py",
        "src/c.py",
    ]
    fetched_paths = [f["path"] for f in fetched]
    assert fetched_paths == expected_order


@patch("app.repository.content_fetcher.get_file_content")
def test_backend_frontend_alternation(mock_get_content):
    mock_get_content.return_value = ("mock content", None)

    files = [
        {"path": "pyproject.toml", "size": 100},
        {"path": "backend/a.py", "size": 100},
        {"path": "backend/b.py", "size": 100},
        {"path": "frontend/c.ts", "size": 100},
        {"path": "frontend/d.ts", "size": 100},
    ]

    fetched = fetch_repository_contents("owner", "repo", files)

    # Round robin should alternate between backend and frontend (sorted alphabetically: backend, frontend)
    expected_order = [
        "pyproject.toml",
        "backend/a.py",
        "frontend/c.ts",
        "backend/b.py",
        "frontend/d.ts",
    ]
    fetched_paths = [f["path"] for f in fetched]
    assert fetched_paths == expected_order


@patch("app.repository.content_fetcher.get_file_content")
def test_exhausted_component_redistributes_budget(mock_get_content):
    mock_get_content.return_value = ("mock content", None)

    files = [
        {"path": "pyproject.toml", "size": 100},
        {"path": "comp_small/a.py", "size": 100}, # Only 1 file
        {"path": "comp_large/b.py", "size": 100},
        {"path": "comp_large/c.py", "size": 100},
        {"path": "comp_large/d.py", "size": 100},
    ]

    fetched = fetch_repository_contents("owner", "repo", files)

    # Round-robin:
    # 1. comp_large/b.py (alphabetical: comp_large, comp_small)
    # 2. comp_small/a.py
    # 3. comp_large/c.py (comp_small is exhausted, remaining budget redistributed)
    # 4. comp_large/d.py
    expected_order = [
        "pyproject.toml",
        "comp_large/b.py",
        "comp_small/a.py",
        "comp_large/c.py",
        "comp_large/d.py",
    ]
    fetched_paths = [f["path"] for f in fetched]
    assert fetched_paths == expected_order


@patch("app.repository.content_fetcher.get_file_content")
def test_pydantic_component_structure(mock_get_content):
    mock_get_content.return_value = ("mock content", None)

    files = [
        {"path": "pydantic-core/Cargo.toml", "size": 100},
        {"path": "pydantic-core/src/lib.rs", "size": 100},
        {"path": "pydantic-core/src/other.rs", "size": 100},
        {"path": "pydantic/a.py", "size": 100},
        {"path": "pydantic/b.py", "size": 100},
    ]

    fetched = fetch_repository_contents("owner", "repo", files)

    # pydantic-core/Cargo.toml is manifest (fetched first)
    # components sorted: pydantic, pydantic-core
    # 1. pydantic/a.py
    # 2. pydantic-core/src/lib.rs
    # 3. pydantic/b.py
    # 4. pydantic-core/src/other.rs
    expected_order = [
        "pydantic-core/Cargo.toml",
        "pydantic/a.py",
        "pydantic-core/src/lib.rs",
        "pydantic/b.py",
        "pydantic-core/src/other.rs",
    ]
    fetched_paths = [f["path"] for f in fetched]
    assert fetched_paths == expected_order
