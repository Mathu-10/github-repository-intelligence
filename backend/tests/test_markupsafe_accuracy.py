from app.analysis.python_parser import parse_python_file
from app.analysis.file_classifier import classify_file

def test_nested_imports_in_try_except():
    content = """
try:
    from ._speedups import escape
except ImportError:
    from ._native import escape
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "._speedups.escape" in result["imports"]
    assert "._native.escape" in result["imports"]

def test_nested_import_in_if():
    content = """
if SOME_CONDITION:
    import typing_extensions as te
else:
    import typing as te
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "typing_extensions" in result["imports"]
    assert "typing" in result["imports"]

def test_import_inside_function_ignored():
    content = """
def my_func():
    import json
    return json.dumps({})
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "json" not in result["imports"]

def test_import_inside_class_method_ignored():
    content = """
class MyClass:
    def method(self):
        import math
        return math.sin(0)
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "math" not in result["imports"]

def test_existing_top_level_absolute_imports():
    content = "import os\nimport sys\n"
    result = parse_python_file(content)
    assert result["success"] is True
    assert "os" in result["imports"]
    assert "sys" in result["imports"]

def test_existing_top_level_relative_imports():
    content = "from .utils import helper\n"
    result = parse_python_file(content)
    assert result["success"] is True
    assert ".utils.helper" in result["imports"]

def test_setup_py_classification():
    assert classify_file("setup.py") == "configuration"
    assert classify_file("setup.cfg") == "configuration"
    assert classify_file("backend/setup.py") == "configuration"

def test_benchmark_classification():
    assert classify_file("bench.py") == "example"
    assert classify_file("benchmarks/run.py") == "example"
    assert classify_file("src/benchmark_utils.py") == "example"
    assert classify_file("bench/bench_markup.py") == "example"
    # Ensure unrelated workbench is not matched
    assert classify_file("src/workbench.py") == "source_code"

def test_normal_production_file_classification():
    assert classify_file("src/markupsafe/_native.py") == "source_code"
    assert classify_file("backend/app/main.py") == "source_code"

def test_tooling_release_classification():
    assert classify_file("release/shared.py") == "other"
    assert classify_file("releases/prepare.py") == "other"
    assert classify_file("tools/build.py") == "other"
    assert classify_file("tooling/format.py") == "other"
    assert classify_file("tasks/publish.py") == "other"
    assert classify_file("scripts/deploy.py") == "other"


def test_typing_type_checking_ignored():
    content = """
import typing
if typing.TYPE_CHECKING:
    import typing_extensions as te
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "typing_extensions" not in result["imports"]


def test_t_type_checking_ignored():
    content = """
import typing as t
if t.TYPE_CHECKING:
    import typing_extensions as te
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "typing_extensions" not in result["imports"]


def test_tp_type_checking_ignored():
    content = """
import typing as tp
if tp.TYPE_CHECKING:
    import typing_extensions as te
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "typing_extensions" not in result["imports"]


def test_imported_type_checking_ignored():
    content = """
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import typing_extensions as te
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "typing_extensions" not in result["imports"]


def test_aliased_type_checking_ignored():
    content = """
from typing import TYPE_CHECKING as TC
if TC:
    import typing_extensions as te
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "typing_extensions" not in result["imports"]


def test_type_checking_else_branch_detected():
    content = """
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import static_only
else:
    import runtime_only
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "static_only" not in result["imports"]
    assert "runtime_only" in result["imports"]


def test_normal_runtime_if_block_detected():
    content = """
if sys.version_info >= (3, 10):
    import runtime_if_module
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "runtime_if_module" in result["imports"]


def test_try_except_imports_detected():
    content = """
try:
    import try_module
except ImportError:
    import except_module
"""
    result = parse_python_file(content)
    assert result["success"] is True
    assert "try_module" in result["imports"]
    assert "except_module" in result["imports"]


from app.analysis.entry_point_detector import detect_entry_points

def test_app_py_library_impl_not_entry_point():
    files = [{
        "path": "src/flask/app.py",
        "category": "source_code",
        "content": "class Flask:\n    pass\ndef run():\n    pass\n"
    }]
    result = detect_entry_points(files)
    assert len(result) == 0

def test_nested_app_py_no_signals_not_entry_point():
    files = [{
        "path": "package/internal/app.py",
        "category": "source_code",
        "content": "# some implementation code here\n"
    }]
    result = detect_entry_points(files)
    assert len(result) == 0

def test_app_py_with_initialization_is_entry_point():
    files = [{
        "path": "app.py",
        "category": "source_code",
        "content": "from fastapi import FastAPI\napp = FastAPI()\n"
    }]
    result = detect_entry_points(files)
    assert len(result) == 1
    assert result[0]["path"] == "app.py"

def test_main_py_remains_entry_point():
    files = [{
        "path": "main.py",
        "category": "source_code",
        "content": "if __name__ == '__main__':\n    pass\n"
    }]
    result = detect_entry_points(files)
    assert len(result) == 1
    assert result[0]["path"] == "main.py"

def test_main_py_no_signals_not_entry_point():
    files = [{
        "path": "main.py",
        "category": "source_code",
        "content": "# main application startup\n"
    }]
    result = detect_entry_points(files)
    assert len(result) == 0

def test_main_py_packages_preserved():
    files = [{
        "path": "src/flask/__main__.py",
        "category": "source_code",
        "content": "if __name__ == '__main__':\n    main()\n"
    }]
    result = detect_entry_points(files)
    assert len(result) == 1
    assert result[0]["path"] == "src/flask/__main__.py"

def test_wsgi_py_ambiguity_needs_signal():
    files_no_signal = [{
        "path": "wsgi.py",
        "category": "source_code",
        "content": "# WSGI server config\n"
    }]
    assert len(detect_entry_points(files_no_signal)) == 0

    files_with_signal = [{
        "path": "wsgi.py",
        "category": "source_code",
        "content": "if __name__ == '__main__':\n    app.run()\n"
    }]
    assert len(detect_entry_points(files_with_signal)) == 1
