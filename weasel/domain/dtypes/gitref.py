import re

from typing import Annotated

from pydantic import AfterValidator


def _validate(ref: str) -> str:
    """Validate the Git reference."""
    if not ref:
        detail = "The reference (branch / tag) cannot be empty"
        raise ValueError(detail)

    if ref.startswith("/") or ref.endswith("/"):
        detail = "The reference (branch / tag) must not start or end with '/'"
        raise ValueError(detail)

    if "//" in ref or ".." in ref:
        detail = "The reference (branch / tag) must not contain '//' and '.."
        raise ValueError(detail)

    if ref.endswith(".lock"):
        detail = "The reference (branch / tag) must not end with '.lock'"
        raise ValueError(detail)

    if re.search(r"[\000-\037\177\s~^:?*\[\\]", ref):
        detail = "The reference (branch / tag) contains unsupported characters"
        raise ValueError(detail)

    if "@{" in ref:
        detail = "The reference (branch / tag) must not contain '@{'"
        raise ValueError(detail)

    if any(part.startswith(".") or part.endswith(".") for part in ref.split("/")):
        detail = "The reference (branch / tag) must not contain '.' at the start or end of any part"
        raise ValueError(detail)

    return ref


GitRef = Annotated[str, AfterValidator(_validate)]
