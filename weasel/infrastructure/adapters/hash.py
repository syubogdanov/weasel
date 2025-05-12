import asyncio

from dataclasses import dataclass
from typing import ClassVar

from blake3 import blake3

from weasel.domain.services.interfaces.hash import HashInterface


@dataclass
class HashAdapter(HashInterface):
    """The hash adapter."""

    _max_threads: int

    _encoding: ClassVar[str] = "utf-8"

    async def hash(self, text: str) -> str:
        """Hash the given text.

        Notes
        -----
        * `blake3` is written in *Rust*.
        """
        data = text.encode(self._encoding)
        hash_ = await asyncio.to_thread(blake3, data, max_threads=self._max_threads)
        return hash_.hexdigest()
