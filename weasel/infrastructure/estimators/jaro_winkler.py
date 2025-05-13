import asyncio

from contextlib import suppress
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from rapidfuzz.distance.JaroWinkler import normalized_similarity

from weasel.domain.services.exceptions import WeaselCacheError
from weasel.domain.services.interfaces.estimator import EstimatorInterface


if TYPE_CHECKING:
    from weasel.domain.dtypes.probability import Probability
    from weasel.domain.services.interfaces.cache import CacheInterface
    from weasel.domain.services.interfaces.hash import HashInterface


@dataclass
class JaroWinklerEstimator(EstimatorInterface):
    """The Jaro-Winkler estimator."""

    _cache: "CacheInterface"
    _hash: "HashInterface"
    _precision: int

    _bucket: ClassVar[str] = "jaro_winkler"

    async def estimate(self, source: str, target: str) -> "Probability":
        """Estimate whether `source` is derived from `target`.

        Notes
        -----
        * `rapidfuzz` is written in *C++*.
        """
        key = await self._build_key(source, target)

        if cached := await self._get_from_cache(key):
            return round(cached, self._precision)

        probability = await asyncio.to_thread(normalized_similarity, source, target)
        await self._put_to_cache(key, probability)

        return round(probability, self._precision)

    async def _build_key(self, source: str, target: str) -> str:
        """Build a cache key for the given source and target strings."""
        key1, key2 = await asyncio.gather(self._hash.hash(source), self._hash.hash(target))
        return f"{key1}:{key2}"

    async def _get_from_cache(self, key: str) -> float | None:
        """Get a cached value for the given key."""
        try:
            cached = await self._cache.get(self._bucket, key)
            return float(cached) if cached else None

        except (ValueError, TypeError, WeaselCacheError):
            return None

    async def _put_to_cache(self, key: str, probability: float) -> None:
        """Put a value into the cache."""
        with suppress(WeaselCacheError):
            await self._cache.put(self._bucket, key, str(probability))
