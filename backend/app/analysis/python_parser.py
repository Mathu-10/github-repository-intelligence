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

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imports.append(
                    f"{module}.{alias.name}" if module else alias.name
                )

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "name": node.name,
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
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
                    (ast.FunctionDef, ast.AsyncFunctionDef),
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