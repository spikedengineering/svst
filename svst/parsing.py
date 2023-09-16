import ast

from typing import List, Dict, Union, Optional

from constants import STANDARD_LOGGING_LEVEL

from output import output_structure_constructor


class ParentNodeTransformer(ast.NodeTransformer):
    def visit(self, node):
        child: ast.NodeVisitor
        for child in ast.iter_child_nodes(node):
            child.parent = node
        return super().visit(node)


class StaticTypeEnforcer(ast.NodeVisitor):
    def __init__(
        self,
        file_name: Optional[str] = None,
        logging_level: str = STANDARD_LOGGING_LEVEL,
    ) -> None:
        self.scope: str = "global"
        self.assignments: Dict[str, set] = {"global": set()}
        self.type_annotations: Dict[str, set] = {"global": set()}

        self.file_name = file_name
        self.logging_level = logging_level

        self.output: List[Dict[str, Union[str, int]]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        previous_scope = self.scope
        self.scope = node.name
        self.assignments[self.scope] = set()
        self.type_annotations[self.scope] = set()
        self.generic_visit(node)
        self.scope = previous_scope

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            self.type_annotations[self.scope].add(var_name)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name not in self.type_annotations[self.scope]:
                if var_name not in self.assignments[self.scope]:
                    self.output.append(
                        output_structure_constructor(
                            self.file_name,
                            node.lineno,
                            var_name,
                            self.scope,
                            self.logging_level,
                        )
                    )
                self.assignments[self.scope].add(var_name)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            if var_name not in self.type_annotations[self.scope]:
                self.output.append(
                    output_structure_constructor(
                        self.file_name,
                        node.lineno,
                        var_name,
                        self.scope,
                        self.logging_level,
                    )
                )
        if isinstance(node.target, ast.Tuple):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    var_name = elt.id
                    if var_name not in self.type_annotations[self.scope]:
                        self.output.append(
                            output_structure_constructor(
                                self.file_name,
                                node.lineno,
                                var_name,
                                self.scope,
                                self.logging_level,
                            )
                        )

        self.generic_visit(node)
