from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from stat import S_ISDIR, S_ISLNK, S_ISREG
from typing import TYPE_CHECKING
from uuid import UUID

from aioshutil import copy2, copytree, rmtree
from aiostdlib import os

from weasel.domain.services.interfaces.sealer import SealerInterface


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.language import LanguageInterface


@dataclass
class SealerAdapter(SealerInterface):
    """The sealer adapter."""

    _data_dir: Path
    _id_factory: Callable[[], UUID]
    _languages: list["LanguageInterface"]

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

        if S_ISREG(st.st_mode):
            await os.makedirs(seal)
            await copy2(path, seal / path.name, follow_symlinks=False)

        if S_ISDIR(st.st_mode):
            await copytree(
                src=path,
                dst=seal,
                symlinks=False,
                ignore=self._ignore,
                ignore_dangling_symlinks=True,
            )

        return seal

    async def clean(self) -> None:
        """Clean the sealing layer."""
        await rmtree(self._seal_dir, ignore_errors=True)  # type: ignore[call-arg]

    def _ignore(self, _dirname: str, files: list[str]) -> bool:
        """Ignore specific patterns when copying trees."""
        suffixes = [suffix for language in self._languages for suffix in language.get_extensions()]
        return [file for file in files if Path(file).suffix not in suffixes]
