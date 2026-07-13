from app.analysis.dependency_analyzer import build_python_dependency_graph


def test_absolute_import_resolves_only_to_specific_module():
    # 1. import flask.cli produces ONLY cli.py and never __init__.py.
    files = [
        {
            "path": "src/flask/__init__.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/flask/cli.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/flask/__main__.py",
            "analysis": {"success": True, "imports": ["flask.cli"]}
        }
    ]

    relationships = build_python_dependency_graph(files)

    # There should only be one relationship: __main__.py -> cli.py
    assert len(relationships) == 1
    rel = relationships[0]
    assert rel["source"] == "src/flask/__main__.py"
    assert rel["target"] == "src/flask/cli.py"
    assert rel["import"] == "flask.cli"


def test_absolute_import_resolves_to_most_specific():
    # 2. import package.subpackage.module always resolves to the most specific module.
    files = [
        {
            "path": "src/package/__init__.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/package/subpackage/__init__.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/package/subpackage/module.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/main.py",
            "analysis": {"success": True, "imports": ["package.subpackage.module"]}
        }
    ]

    relationships = build_python_dependency_graph(files)

    # Must resolve only to package/subpackage/module.py
    assert len(relationships) == 1
    rel = relationships[0]
    assert rel["source"] == "src/main.py"
    assert rel["target"] == "src/package/subpackage/module.py"


def test_relative_import_resolves_to_deepest():
    # 3. from .core.config import Settings resolves to core/config.py instead of core/__init__.py.
    files = [
        {
            "path": "src/core/__init__.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/core/config.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/utils.py",
            "analysis": {"success": True, "imports": [".core.config.Settings"]}
        }
    ]

    relationships = build_python_dependency_graph(files)

    # Must resolve to core/config.py, not core/__init__.py
    assert len(relationships) == 1
    rel = relationships[0]
    assert rel["source"] == "src/utils.py"
    assert rel["target"] == "src/core/config.py"


def test_relative_import_double_dot_resolves_to_deepest():
    # 4. from ..utils.helpers import foo resolves to the deepest valid module.
    files = [
        {
            "path": "src/app/utils/__init__.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/app/utils/helpers.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/app/controllers/user.py",
            "analysis": {"success": True, "imports": ["..utils.helpers.foo"]}
        }
    ]

    relationships = build_python_dependency_graph(files)

    # Must resolve to src/app/utils/helpers.py
    assert len(relationships) == 1
    rel = relationships[0]
    assert rel["source"] == "src/app/controllers/user.py"
    assert rel["target"] == "src/app/utils/helpers.py"


def test_duplicate_edges_are_never_created():
    # 5. Duplicate dependency edges are never created.
    files = [
        {
            "path": "src/flask/cli.py",
            "analysis": {"success": True, "imports": []}
        },
        {
            "path": "src/flask/__main__.py",
            "analysis": {"success": True, "imports": ["flask.cli", "flask.cli"]}
        }
    ]

    relationships = build_python_dependency_graph(files)

    # There should only be one relationship despite duplicate import entries
    assert len(relationships) == 1
    rel = relationships[0]
    assert rel["source"] == "src/flask/__main__.py"
    assert rel["target"] == "src/flask/cli.py"
