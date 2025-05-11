from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Selector, Singleton

from weasel.infrastructure.estimators.damerau_levenshtein import DamerauLevenshteinEstimator
from weasel.infrastructure.estimators.jaro_winkler import JaroWinklerEstimator
from weasel.infrastructure.estimators.levenshtein import LevenshteinEstimator
from weasel.infrastructure.mutations.python import py001, py002, py003, py004, py005, py006
from weasel.infrastructure.mutations.starlark import bzl001, bzl002, bzl003, bzl004, bzl005
from weasel.settings import WeaselSettings


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.mutation import MutationInterface


class WeaselContainer(DeclarativeContainer):
    """The dependency injection container."""

    weasel_settings: Provider["WeaselSettings"] = Singleton(WeaselSettings)

    damerau_levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(
        DamerauLevenshteinEstimator
    )
    jaro_winkler_estimator: Provider["EstimatorInterface"] = Singleton(JaroWinklerEstimator)
    levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(LevenshteinEstimator)

    estimator: Provider["EstimatorInterface"] = Selector(
        weasel_settings.provided.estimator_type,
        damerau_levenshtein=damerau_levenshtein_estimator.provided,
        jaro_winkler=jaro_winkler_estimator.provided,
        levenshtein=levenshtein_estimator.provided,
    )

    bzl001: Provider["MutationInterface"] = Singleton(bzl001.StarlarkMutation)
    bzl002: Provider["MutationInterface"] = Singleton(bzl002.StarlarkMutation)
    bzl003: Provider["MutationInterface"] = Singleton(bzl003.StarlarkMutation)
    bzl004: Provider["MutationInterface"] = Singleton(bzl004.StarlarkMutation)
    bzl005: Provider["MutationInterface"] = Singleton(bzl005.StarlarkMutation)

    py001: Provider["MutationInterface"] = Singleton(py001.PythonMutation)
    py002: Provider["MutationInterface"] = Singleton(py002.PythonMutation)
    py003: Provider["MutationInterface"] = Singleton(py003.PythonMutation)
    py004: Provider["MutationInterface"] = Singleton(py004.PythonMutation)
    py005: Provider["MutationInterface"] = Singleton(py005.PythonMutation)
    py006: Provider["MutationInterface"] = Singleton(
        py006.PythonMutation, _estimator=estimator.provided
    )


WEASEL_CONTAINER = WeaselContainer()
