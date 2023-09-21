import ast

from svst import output


class VariableAnnotationChecker(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.annotated_vars = set()
        self.scope_stack = []
        self.error_messages = []

    def enter_scope(self, scope_name):
        self.scope_stack.append(scope_name)

    def exit_scope(self):
        self.scope_stack.pop()

    def current_scope(self):
        return ".".join(self.scope_stack)

    def generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        item.parent = node
                        self.visit(item)
            elif isinstance(value, ast.AST):
                value.parent = node
                self.visit(value)

    def report(self, node, message):
        current_scope = self.current_scope()
        full_scope = ".".join(self.scope_stack)
        self.error_messages.append(
            output.output_structure_constructor(
                self.filename,
                node.lineno,
                message,
                full_scope,
            )
        )

    def check_target(self, node):
        if isinstance(node, (ast.Tuple, ast.List)):
            for el in node.elts:
                self.check_target(el)
        elif isinstance(node, ast.Name):
            if node.id not in self.annotated_vars:
                self.report(node, f'Variable "{node.id}"')
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                self.check_target(target)

    def visit_AnnAssign(self, node):
        if node.simple and node.target and isinstance(node.target, ast.Name):
            self.annotated_vars.add(node.target.id)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            self.check_target(target)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self.check_target(node.target)
        self.generic_visit(node)

    def visit_For(self, node):
        self.check_target(node.target)
        self.generic_visit(node)

    def visit_With(self, node):
        for item in node.items:
            if item.optional_vars:
                self.check_target(item.optional_vars)
        self.generic_visit(node)

    def visit_Lambda(self, node):
        # No annotation check for Lambda, as they cannot be type annotated.
        pass

    def visit_arg(self, node):
        parent = getattr(node, "parent", None)
        if isinstance(parent, ast.Lambda) or node.arg == "self":
            return
        if not node.annotation:
            self.report(node, f'Function argument "{node.arg}"')
        else:
            self.annotated_vars.add(node.arg)
        self.generic_visit(node)

    def visit_Comprehension(self, node):
        self.check_target(node.target)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.name and not isinstance(node.name, ast.Name):
            self.report(node, f'Exception handler variable "{node.name}"')
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Skip checking annotations for attributes
        pass

    def visit_If(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Check default values in function definitions
        self.enter_scope(node.name)
        for default in node.args.defaults:
            if isinstance(default, ast.Name):
                self.check_target(default)
        self.generic_visit(node)
        self.exit_scope()

    def visit_Try(self, node):
        # Check variables in the 'except' part
        self.enter_scope("try")
        for handler in node.handlers:
            if handler.name and not isinstance(handler.name, ast.Name):
                self.report(
                    handler,
                    f'Exception handler variable "{handler.name}"',
                )
        self.generic_visit(node)
        self.exit_scope()

    def visit_ClassDef(self, node):
        self.enter_scope(node.name)
        self.generic_visit(node)
        self.exit_scope()

    # Checking List, Set, Dict comprehensions
    def visit_ListComp(self, node):
        for comprehension in node.generators:
            self.visit_Comprehension(comprehension)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        for comprehension in node.generators:
            self.visit_Comprehension(comprehension)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        for comprehension in node.generators:
            self.visit_Comprehension(comprehension)
        self.generic_visit(node)

    # Check variables in while loop
    def visit_While(self, node):
        self.enter_scope("while")
        self.check_target(node.test)
        self.generic_visit(node)
        self.exit_scope()
