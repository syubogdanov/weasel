import ast

from dataclasses import dataclass

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`PY002`).

    Features
    --------
    * Removes type annotations.
    """

    @classmethod
    async def mutate(cls, source: str, target: str) -> str:  # noqa: ARG003
        """Mutate `source` using `target` as the reference."""
        tree = ast.parse(source)

        transformer = PythonTransformer()
        tree = transformer.visit(tree)

        if not transformer.is_triggered():
            return source

        tree = ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    @classmethod
    def as_label(cls) -> str:
        """Return the mutation label."""
        return "PY002"


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

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        """Visit an asynchronous function."""
        return self._visit_function(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        """Visit a synchronous function."""
        return self._visit_function(node)

    def _visit_function(self, node: ast.AST) -> ast.AST:
        """Visit a function."""
        node = self.generic_visit(node)

        for arg in node.args.args:
            if arg.annotation is not None:
                arg.annotation = None
                self._triggered = True

        if node.args.vararg is not None:
            node.args.vararg.annotation = None
            self._triggered = True

        if node.args.kwarg is not None:
            node.args.kwarg.annotation = None
            self._triggered = True

        if node.returns is not None:
            node.returns = None
            self._triggered = True

        return node
