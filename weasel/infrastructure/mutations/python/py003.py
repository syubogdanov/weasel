import ast

from dataclasses import dataclass

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`PY003`).

    Features
    --------
    * Removes unused constants.
    """

    def mutate(self, source: str, target: str) -> str:  # noqa: ARG002
        """Mutate `source` using `target` as the reference."""
        tree = ast.parse(source)

        transformer = PythonTransformer()
        tree = transformer.visit(tree)

        if not transformer.is_triggered():
            return source

        tree = ast.fix_missing_locations(tree)
        return ast.unparse(tree)


@dataclass
class PythonTransformer(ast.NodeTransformer):
    """The AST transformer.

    Notes
    -----
    * Consider this class as a private one.
    """

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._triggered: bool = False

    def is_triggered(self) -> bool:
        """Check if any transformation was made."""
        return self._triggered

    def visit_AsyncFor(self, node: ast.AsyncFor) -> ast.AsyncFor:
        """Visit an asynchronous `for`-loop."""
        return self._visit_block(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Visit an asynchronous function."""
        return self._visit_block(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> ast.AsyncWith:
        """Visit an asynchronous `with`-block."""
        return self._visit_block(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Visit a class definition."""
        return self._visit_block(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.ExceptHandler:
        """Visit an `except`-block."""
        return self._visit_block(node)

    def visit_For(self, node: ast.For) -> ast.For:
        """Visit a synchronous `for`-loop."""
        return self._visit_block(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Visit a synchronous function."""
        return self._visit_block(node)

    def visit_If(self, node: ast.If) -> ast.If:
        """Visit an `if`-block."""
        return self._visit_block(node)

    def visit_Module(self, node: ast.Module) -> ast.Module:
        """Visit a global namespace."""
        return self._visit_block(node)

    def visit_Try(self, node: ast.Try) -> ast.Try:
        """Visit a `try`-block."""
        return self._visit_block(node)

    def visit_TryStar(self, node: ast.TryStar) -> ast.TryStar:
        """Visit an `except*`-block."""
        return self._visit_block(node)

    def visit_While(self, node: ast.While) -> ast.While:
        """Visit a `while`-loop."""
        return self._visit_block(node)

    def visit_With(self, node: ast.With) -> ast.With:
        """Visit a synchronous `with`-block."""
        return self._visit_block(node)

    def _visit_block(self, node: ast.AST) -> ast.AST:
        """Visit an AST-block."""
        node = self.generic_visit(node)

        for attribute_name in ("body", "finalbody", "orelse"):
            if body := getattr(node, attribute_name, []):
                children = [child for child in body if not self._is_constant(child)]

                if len(children) < len(body):
                    self._triggered = True
                    children = children or [ast.Pass()]
                    setattr(node, attribute_name, children)

        return node

    @classmethod
    def _is_constant(cls, node: ast.AST | None) -> bool:
        """Check whether `node` is a constant."""
        if isinstance(node, ast.UnaryOp):
            return isinstance(node.operand, ast.Constant)

        if isinstance(node, (ast.List, ast.Set, ast.Tuple)):
            return all(cls._is_constant(elt) for elt in node.elts)

        if isinstance(node, ast.Dict):
            return all(cls._is_constant(key_or_value) for key_or_value in node.keys + node.values)

        if isinstance(node, ast.Expr):
            return cls._is_constant(node.value)

        return isinstance(node, ast.Constant)
