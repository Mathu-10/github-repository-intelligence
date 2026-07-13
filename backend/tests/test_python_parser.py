from app.analysis.python_parser import parse_python_file


def test_absolute_import():
    result = parse_python_file(
        "import fastapi\n"
    )

    assert result["success"] is True
    assert "fastapi" in result["imports"]


def test_relative_import_not_treated_as_external():
    result = parse_python_file(
        "from . import core\n"
    )

    assert result["success"] is True
    assert "core" not in result["imports"]


def test_function_and_class_detection():
    content = """
def hello(name):
    return name


class User:
    def save(self):
        pass
"""

    result = parse_python_file(content)

    assert result["success"] is True
    assert len(result["functions"]) == 1
    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "User"