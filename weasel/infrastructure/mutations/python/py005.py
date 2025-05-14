import ast
import operator

from contextlib import suppress
from dataclasses import dataclass
from functools import reduce

from weasel.domain.services.interfaces.mutation import MutationInterface


@dataclass
class PythonMutation(MutationInterface):
    """The *Python* mutation (`PY005`).

    Features
    --------
    * Simplifies arithmetic operations (`2 + 2` -> `4`).
    """

    @classmethod
    async def mutate(cls, source: str, _target: str) -> str:
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
        return "PY005"


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

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        """Visit a binary operation.

        Notes
        -----
        * Consider this method as a private one.
        """
        node = self.generic_visit(node)

        if not isinstance(node.left, ast.Constant):
            return node

        if not isinstance(node.right, ast.Constant):
            return node

        binary_operators = {
            ast.Add: operator.add,
            ast.BitAnd: operator.and_,
            ast.FloorDiv: operator.floordiv,
            ast.LShift: operator.lshift,
            ast.Mod: operator.mod,
            ast.Mult: operator.mul,
            ast.BitOr: operator.or_,
            ast.Pow: operator.pow,
            ast.RShift: operator.rshift,
            ast.Sub: operator.sub,
            ast.Div: operator.truediv,
            ast.BitXor: operator.xor,
        }

        if not (binary_operator := binary_operators.get(type(node.op))):
            return node

        with suppress(Exception):
            constant = binary_operator(node.left.value, node.right.value)
            node = ast.Constant(constant)
            self._triggered = True

        return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        """Visit a boolean operation.

        Notes
        -----
        * Consider this method as a private one.
        """
        node = self.generic_visit(node)

        if not all(isinstance(child, ast.Constant) for child in node.values):
            return node

        children: list[ast.Constant] = node.values
        values = [child.value for child in children]

        boolean_operators = {ast.And: operator.and_, ast.Or: operator.or_}

        if not (boolean_operator := boolean_operators.get(type(node.op))):
            return node

        with suppress(Exception):
            constant = reduce(boolean_operator, values)
            node = ast.Constant(constant)
            self._triggered = True

        return node

    def visit_UnaryOp(self, node: ast.UnaryOp) -> ast.AST:
        """Visit an unary operation.

        Notes
        -----
        * Consider this method as a private one.
        """
        node = self.generic_visit(node)

        if not isinstance(node.operand, ast.Constant):
            return node

        unary_operators = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
            ast.Not: operator.not_,
            ast.Invert: operator.invert,
        }

        if not (unary_operator := unary_operators.get(type(node.op))):
            return node

        with suppress(Exception):
            constant = unary_operator(node.operand.value)
            node = ast.Constant(constant)
            self._triggered = True

        return node
