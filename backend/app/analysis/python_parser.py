import ast


def parse_python_file(content: str) -> dict:
    try:
        tree = ast.parse(content)
    except SyntaxError as error:
        return {
            "success": False,
            "error": str(error),
            "imports": [],
            "functions": [],
            "classes": [],
        }

    imports = []
    functions = []
    classes = []

    typing_aliases = {"typing"}
    tc_aliases = {"TYPE_CHECKING"}

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "typing":
                    typing_aliases.add(alias.asname or "typing")
        elif isinstance(node, ast.ImportFrom):
            if node.module == "typing":
                for alias in node.names:
                    if alias.name == "TYPE_CHECKING":
                        tc_aliases.add(alias.asname or "TYPE_CHECKING")

    def is_type_checking_condition(test):
        if isinstance(test, ast.Name):
            return test.id in tc_aliases
        if isinstance(test, ast.Attribute):
            if test.attr == "TYPE_CHECKING":
                if isinstance(test.value, ast.Name) and test.value.id in typing_aliases:
                    return True
        return False

    def extract_imports(node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            relative_prefix = "." * node.level
            full_module = f"{relative_prefix}{module}"
            for alias in node.names:
                if full_module:
                    imports.append(f"{full_module}.{alias.name}")
                else:
                    imports.append(f"{relative_prefix}{alias.name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            return
        elif isinstance(node, ast.If):
            if is_type_checking_condition(node.test):
                if hasattr(node, "orelse") and isinstance(node.orelse, list):
                    for child in node.orelse:
                        extract_imports(child)
            else:
                for child in ast.iter_child_nodes(node):
                    extract_imports(child)
        else:
            for child in ast.iter_child_nodes(node):
                extract_imports(child)

    extract_imports(tree)

    for node in ast.iter_child_nodes(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            functions.append({
                "name": node.name,
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "is_async": isinstance(
                    node,
                    ast.AsyncFunctionDef,
                ),
                "arguments": [
                    argument.arg
                    for argument in node.args.args
                ],
            })

        elif isinstance(node, ast.ClassDef):
            methods = []

            for class_node in node.body:
                if isinstance(
                    class_node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):
                    methods.append({
                        "name": class_node.name,
                        "line_start": class_node.lineno,
                        "line_end": class_node.end_lineno,
                        "is_async": isinstance(
                            class_node,
                            ast.AsyncFunctionDef,
                        ),
                        "arguments": [
                            argument.arg
                            for argument in class_node.args.args
                        ],
                    })

            classes.append({
                "name": node.name,
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "base_classes": [
                    ast.unparse(base)
                    for base in node.bases
                ],
                "methods": methods,
            })

    return {
        "success": True,
        "error": None,
        "imports": imports,
        "functions": functions,
        "classes": classes,
    }