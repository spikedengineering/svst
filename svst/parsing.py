import ast

from typing import Dict, Iterator, List, Optional, Set, Tuple, Union
from typing_extensions import TypeAlias

from svst import output


FunctionNode: TypeAlias = Union[ast.FunctionDef, ast.AsyncFunctionDef]
ComprehensionNode: TypeAlias = Union[ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp]

# Nodes that open a new Python name scope.
SCOPE_NODES: Tuple[type, ...] = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Lambda,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
)

MODULE_SCOPE_NAME: str = "global"


def iter_scope_nodes(node: ast.AST) -> Iterator[ast.AST]:
    """Yield every node that belongs to the scope of `node`, without entering nested scopes.

    Args:
        node: Node that opens a scope (module, class, function...).

    Yields:
        Descendant nodes in the same scope.
    """
    stack: List[ast.AST] = list(ast.iter_child_nodes(node))
    while stack:
        child: ast.AST = stack.pop()
        yield child
        if not isinstance(child, SCOPE_NODES):
            stack.extend(ast.iter_child_nodes(child))


class Scope:
    """A Python name scope and the variables explicitly annotated in it.

    Args:
        kind: One of "module", "class", "function", "lambda" or "comprehension".
        name: Qualified name of the scope, used in error messages.
        node: Node that opens the scope.
        parent: Enclosing scope, None for the module.
    """

    def __init__(
        self, kind: str, name: str, node: ast.AST, parent: Optional["Scope"]
    ) -> None:
        self.kind: str = kind
        self.name: str = name
        self.parent: Optional[Scope] = parent
        # Variable name -> line of its first annotation.
        self.declared: Dict[str, int] = {}
        self.global_names: Set[str] = set()
        self.nonlocal_names: Set[str] = set()

        child: ast.AST
        for child in iter_scope_nodes(node):
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                self.declare(child.target.id, child.lineno)
            elif isinstance(child, (ast.Import, ast.ImportFrom)):
                # Imported names are typed where they are defined, and cannot be re-annotated.
                alias: ast.alias
                for alias in child.names:
                    if alias.name != "*":
                        self.declare(alias.asname or alias.name.split(".")[0], child.lineno)
            elif isinstance(child, ast.Global):
                self.global_names.update(child.names)
            elif isinstance(child, ast.Nonlocal):
                self.nonlocal_names.update(child.names)

    @property
    def annotatable(self) -> bool:
        """Lambda parameters and comprehension targets have no annotation syntax."""
        return self.kind not in ("lambda", "comprehension")

    def declare(self, name: str, line_number: int) -> None:
        self.declared[name] = min(line_number, self.declared.get(name, line_number))

    def child_name(self, name: str) -> str:
        return name if self.kind == "module" else f"{self.name}.{name}"


class VariableAnnotationChecker(ast.NodeVisitor):
    """Report every variable binding that was not explicitly annotated beforehand.

    A binding (assignment, loop target, `with ... as`, `except ... as`, walrus,
    `match` capture, function argument) is accepted when the variable has an
    annotation in the scope the binding refers to, on or before the binding line.

    Args:
        file_name: Path of the file being analysed, None for bare code.
    """

    def __init__(self, file_name: Optional[str]) -> None:
        self.file_name: Optional[str] = file_name
        self.scope: Optional[Scope] = None
        self._errors: List[Tuple[int, int, output.OutputTypedDict]] = []

    @property
    def error_messages(self) -> List[output.OutputTypedDict]:
        """Errors sorted by position in the source."""
        return [error[2] for error in sorted(self._errors, key=lambda e: e[:2])]

    # Scope handling

    def _current_scope(self) -> Scope:
        assert self.scope is not None, "visit must start from an ast.Module"
        return self.scope

    def _push_scope(self, kind: str, name: str, node: ast.AST) -> Scope:
        parent: Optional[Scope] = self.scope
        qualified_name: str = parent.child_name(name) if parent else name
        self.scope = Scope(kind, qualified_name, node, parent)
        return self.scope

    def _pop_scope(self) -> None:
        self.scope = self._current_scope().parent

    def _module_scope(self) -> Scope:
        scope: Scope = self._current_scope()
        while scope.parent is not None:
            scope = scope.parent
        return scope

    # Reporting

    def report(self, node: ast.AST, variable_name: str, scope: Scope) -> None:
        line_number: int = getattr(node, "lineno", 0)
        column: int = getattr(node, "col_offset", 0)
        self._errors.append(
            (
                line_number,
                column,
                output.output_structure_constructor(
                    self.file_name, line_number, variable_name, scope.name
                ),
            )
        )

    def _is_declared(self, name: str, line_number: int, scope: Scope) -> bool:
        if name in scope.global_names:
            return name in self._module_scope().declared

        if name in scope.nonlocal_names:
            enclosing: Optional[Scope] = scope.parent
            while enclosing is not None:
                if enclosing.kind == "function" and name in enclosing.declared:
                    return True
                enclosing = enclosing.parent
            return False

        return scope.declared.get(name, line_number + 1) <= line_number

    def check_name(self, name: str, node: ast.AST, scope: Optional[Scope] = None) -> None:
        """Report `name` if it is bound at `node` without a previous annotation."""
        scope = scope or self._current_scope()
        if not scope.annotatable:
            return
        if not self._is_declared(name, getattr(node, "lineno", 0), scope):
            self.report(node, name, scope)

    def check_target(self, node: ast.AST) -> None:
        """Check an assignment target; attributes and subscripts are not variables."""
        if isinstance(node, ast.Name):
            self.check_name(node.id, node)
        elif isinstance(node, (ast.Tuple, ast.List)):
            element: ast.AST
            for element in node.elts:
                self.check_target(element)
        elif isinstance(node, ast.Starred):
            self.check_target(node.value)

    # Scopes

    def visit_Module(self, node: ast.Module) -> None:
        self._push_scope("module", MODULE_SCOPE_NAME, node)
        self.generic_visit(node)
        self._pop_scope()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        expression: ast.AST
        for expression in [*node.decorator_list, *node.bases, *node.keywords]:
            self.visit(expression)

        self._push_scope("class", node.name, node)
        statement: ast.stmt
        for statement in node.body:
            self.visit(statement)
        self._pop_scope()

    def _visit_function(self, node: FunctionNode) -> None:
        enclosing: Scope = self._current_scope()

        # Decorators, defaults and annotations are evaluated in the enclosing scope.
        expression: Optional[ast.AST]
        for expression in [
            *node.decorator_list,
            *node.args.defaults,
            *node.args.kw_defaults,
            node.returns,
        ]:
            if expression is not None:
                self.visit(expression)

        arguments: List[ast.arg] = [
            *getattr(node.args, "posonlyargs", []),
            *node.args.args,
            *node.args.kwonlyargs,
        ]
        if node.args.vararg:
            arguments.append(node.args.vararg)
        if node.args.kwarg:
            arguments.append(node.args.kwarg)

        argument: ast.arg
        for argument in arguments:
            if argument.annotation is not None:
                self.visit(argument.annotation)

        scope: Scope = self._push_scope("function", node.name, node)

        implicit_first_argument: bool = enclosing.kind == "class" and not any(
            isinstance(decorator, ast.Name) and decorator.id == "staticmethod"
            for decorator in node.decorator_list
        )
        positional: List[ast.arg] = [
            *getattr(node.args, "posonlyargs", []),
            *node.args.args,
        ]

        for argument in arguments:
            is_self_or_cls: bool = (
                implicit_first_argument and bool(positional) and argument is positional[0]
            )
            if argument.annotation is None and not is_self_or_cls:
                self.report(argument, argument.arg, scope)
            # Declared either way so the argument is reported only once.
            scope.declare(argument.arg, 0)

        statement: ast.stmt
        for statement in node.body:
            self.visit(statement)
        self._pop_scope()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        default: Optional[ast.expr]
        for default in [*node.args.defaults, *node.args.kw_defaults]:
            if default is not None:
                self.visit(default)

        self._push_scope("lambda", "<lambda>", node)
        self.visit(node.body)
        self._pop_scope()

    def _visit_comprehension(self, node: ComprehensionNode) -> None:
        self._push_scope("comprehension", "<comprehension>", node)
        self.generic_visit(node)
        self._pop_scope()

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node)

    # Bindings

    def visit_Assign(self, node: ast.Assign) -> None:
        target: ast.expr
        for target in node.targets:
            self.check_target(target)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.check_target(node.target)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.check_target(node.target)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.check_target(node.target)
        self.generic_visit(node)

    def visit_withitem(self, node: ast.withitem) -> None:
        if node.optional_vars is not None:
            self.check_target(node.optional_vars)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.name:
            self.check_name(node.name, node)
        self.generic_visit(node)

    def visit_NamedExpr(self, node: ast.AST) -> None:
        # A walrus inside a comprehension binds in the enclosing scope.
        scope: Optional[Scope] = self._current_scope()
        while scope is not None and scope.kind == "comprehension":
            scope = scope.parent

        target: ast.AST = getattr(node, "target")
        if scope is not None and isinstance(target, ast.Name):
            self.check_name(target.id, target, scope)
        self.generic_visit(node)

    def visit_MatchAs(self, node: ast.AST) -> None:
        name: Optional[str] = getattr(node, "name", None)
        if name:
            self.check_name(name, node)
        self.generic_visit(node)

    def visit_MatchStar(self, node: ast.AST) -> None:
        name: Optional[str] = getattr(node, "name", None)
        if name:
            self.check_name(name, node)
        self.generic_visit(node)

    def visit_MatchMapping(self, node: ast.AST) -> None:
        rest: Optional[str] = getattr(node, "rest", None)
        if rest:
            self.check_name(rest, node)
        self.generic_visit(node)
