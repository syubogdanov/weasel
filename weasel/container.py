from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton

from weasel.infrastructure.estimators.levenshtein import LevenshteinEstimator


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface


class WeaselContainer(DeclarativeContainer):
    """The dependency injection container."""

    levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(LevenshteinEstimator)


WEASEL_CONTAINER = WeaselContainer()
