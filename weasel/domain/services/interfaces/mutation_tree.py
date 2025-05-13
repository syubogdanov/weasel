from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.mutation import MutationInterface


class MutationTreeInterface(Protocol):
    """The mutation tree interface."""

    @abstractmethod
    async def get_mutations(self, source: str, target: str) -> list["MutationInterface"]:
        """Get the set of mutations required to convert `source` to `target`."""
