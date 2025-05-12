from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from stat import S_ISDIR, S_ISLNK, S_ISREG
from uuid import UUID

from aioshutil import copy2, copytree, rmtree
from aiostdlib import os

from weasel.domain.services.interfaces.sealer import SealerInterface


@dataclass
class SealerAdapter(SealerInterface):
    """The sealer adapter."""

    _data_dir: Path
    _id_factory: Callable[[], UUID]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._seal_dir = self._data_dir / "seal"

    async def seal(self, path: Path) -> Path:
        """Seal the file or directory."""
        try:
            st = await os.lstat(path)

        except (OSError, ValueError) as exception:
            detail = f"'{path}' does not exist"
            raise FileNotFoundError(detail) from exception

        if S_ISLNK(st.st_mode):
            detail = f"'{path}' is a symbolic link"
            raise OSError(detail)

        if not S_ISREG(st.st_mode) and not S_ISDIR(st.st_mode):
            detail = f"'{path}' is not a regular file or directory"
            raise OSError(detail)

        if S_ISDIR(st.st_mode) and not await os.listdir(path):
            detail = f"'{path}' is an empty directory"
            raise OSError(detail)

        identifier = self._id_factory()
        seal = self._seal_dir / identifier.hex
        await os.makedirs(seal)

        if S_ISREG(st.st_mode):
            await copy2(path, seal / path.name)

        if S_ISDIR(st.st_mode):
            await copytree(path, seal / path.name, symlinks=False, ignore_dangling_symlinks=True)

        return seal

    async def clean(self) -> None:
        """Clean the sealing layer."""
        await rmtree(self._seal_dir, ignore_errors=True)
