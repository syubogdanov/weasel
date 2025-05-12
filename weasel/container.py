from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import List, Provider, Selector, Singleton

from weasel.domain.services.mutation_tree import MutationTree
from weasel.infrastructure.estimators.damerau_levenshtein import DamerauLevenshteinEstimator
from weasel.infrastructure.estimators.jaro_winkler import JaroWinklerEstimator
from weasel.infrastructure.estimators.levenshtein import LevenshteinEstimator
from weasel.infrastructure.languages.java import JavaLanguage
from weasel.infrastructure.languages.python import PythonLanguage
from weasel.infrastructure.languages.sql import SQLLanguage
from weasel.infrastructure.languages.starlark import StarlarkLanguage
from weasel.infrastructure.mutations.java import java001
from weasel.infrastructure.mutations.python import py001, py002, py003, py004, py005, py006
from weasel.infrastructure.mutations.starlark import bzl001, bzl002, bzl003, bzl004, bzl005
from weasel.settings.core import CoreSettings
from weasel.settings.mutation_tree import MutationTreeSettings
from weasel.settings.retries import RetriesSettings


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.language import LanguageInterface
    from weasel.domain.services.interfaces.mutation import MutationInterface


class WeaselContainer(DeclarativeContainer):
    """The dependency injection container."""

    core_settings: Provider["CoreSettings"] = Singleton(CoreSettings)
    mutation_tree_settings: Provider["MutationTreeSettings"] = Singleton(MutationTreeSettings)
    retries_settings: Provider["RetriesSettings"] = Singleton(RetriesSettings)

    damerau_levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(
        DamerauLevenshteinEstimator
    )
    jaro_winkler_estimator: Provider["EstimatorInterface"] = Singleton(JaroWinklerEstimator)
    levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(LevenshteinEstimator)

    java_language: Provider["LanguageInterface"] = Singleton(JavaLanguage)
    python_language: Provider["LanguageInterface"] = Singleton(PythonLanguage)
    sql_language: Provider["LanguageInterface"] = Singleton(SQLLanguage)
    starlark_language: Provider["LanguageInterface"] = Singleton(StarlarkLanguage)

    estimator: Provider["EstimatorInterface"] = Selector(
        core_settings.provided.estimator_type,
        damerau_levenshtein=damerau_levenshtein_estimator.provided,
        jaro_winkler=jaro_winkler_estimator.provided,
        levenshtein=levenshtein_estimator.provided,
    )

    bzl001: Provider["MutationInterface"] = Singleton(bzl001.StarlarkMutation)
    bzl002: Provider["MutationInterface"] = Singleton(bzl002.StarlarkMutation)
    bzl003: Provider["MutationInterface"] = Singleton(bzl003.StarlarkMutation)
    bzl004: Provider["MutationInterface"] = Singleton(bzl004.StarlarkMutation)
    bzl005: Provider["MutationInterface"] = Singleton(
        bzl005.StarlarkMutation, _estimator=estimator.provided
    )

    java001: Provider["MutationInterface"] = Singleton(java001.JavaMutation)

    py001: Provider["MutationInterface"] = Singleton(py001.PythonMutation)
    py002: Provider["MutationInterface"] = Singleton(py002.PythonMutation)
    py003: Provider["MutationInterface"] = Singleton(py003.PythonMutation)
    py004: Provider["MutationInterface"] = Singleton(py004.PythonMutation)
    py005: Provider["MutationInterface"] = Singleton(py005.PythonMutation)
    py006: Provider["MutationInterface"] = Singleton(
        py006.PythonMutation, _estimator=estimator.provided
    )

    java_mutations: Provider[list["MutationInterface"]] = List(java001.provided)
    python_mutations: Provider[list["MutationInterface"]] = List(
        py001.provided,
        py002.provided,
        py003.provided,
        py004.provided,
        py005.provided,
        py006.provided,
    )
    starlark_mutations: Provider[list["MutationInterface"]] = List(
        bzl001.provided, bzl002.provided, bzl003.provided, bzl004.provided, bzl005.provided
    )
    sql_mutations: Provider[list["MutationInterface"]] = List()

    java_mutation_tree: Provider["MutationTree"] = Singleton(
        MutationTree,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=java_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    python_mutation_tree: Provider["MutationTree"] = Singleton(
        MutationTree,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=python_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    starlark_mutation_tree: Provider["MutationTree"] = Singleton(
        MutationTree,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=starlark_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    sql_mutation_tree: Provider["MutationTree"] = Singleton(
        MutationTree,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=sql_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )


WEASEL_CONTAINER = WeaselContainer()
