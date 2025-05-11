import ast

from dataclasses import dataclass
from typing import TYPE_CHECKING

from weasel.domain.services.interfaces.mutation import MutationInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`PY006`).

    Features
    --------
    * Eliminates syntatic permutations.

    Notes
    -----
    * Null-augmented block comparison is used.
    """

    _estimator: "EstimatorInterface"

    def mutate(self, source: str, target: str) -> str:
        """Mutate `source` using `target` as the reference."""
        source_tree = ast.parse(source)
        target_tree = ast.parse(target)

        reorderer = PythonReorderer(_estimator=self._estimator)
        tree = reorderer.reorder_tree(source_tree, target_tree)

        if not reorderer.is_triggered():
            return source

        tree = ast.fix_missing_locations(tree)
        return ast.unparse(tree)


@dataclass
class PythonReorderer:
    """The AST reorderer.

    Notes
    -----
    * Consider this class as a private one.
    """

    _estimator: "EstimatorInterface"

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._triggered: bool = False

    def is_triggered(self) -> bool:
        """Check if any permutation was made."""
        return self._triggered

    def reorder_tree(self, source: ast.Module, target: ast.Module) -> ast.Module:
        """Reorder `source` using `target` as the reference."""
        body = self._reorder_list(source.body, target.body)
        return ast.Module(body=body, type_ignores=source.type_ignores)

    def _reorder_list(self, source: list[ast.AST], target: list[ast.AST]) -> list[ast.AST]:  # noqa: ARG002
        """Reorder `source` using `target` as the reference."""
        return source

    def _reorder_class(self, source: ast.ClassDef, target: ast.ClassDef) -> ast.ClassDef:
        """Reorder `source` using `target` as the reference."""
        return ast.ClassDef(
            name=source.name,
            bases=source.bases,
            keywords=source.keywords,
            body=self._reorder_list(source.body, target.body),
            decorator_list=source.decorator_list,
            type_params=source.type_params,
        )

    def _compare_blocks(
        self, source: ast.AST | list[ast.AST], target: ast.AST | list[ast.AST]
    ) -> float:
        """Compare `source` and `target` blocks."""
        if isinstance(source, ast.ClassDef) and isinstance(target, ast.ClassDef):
            source = self._reorder_class(source, target)
        return self._estimator.estimate(ast.unparse(source), ast.unparse(target))
