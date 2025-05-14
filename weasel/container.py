from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory, List, Provider, Selector, Singleton

from weasel.domain.services.scanner import ScannerService
from weasel.domain.types.language import LanguageType
from weasel.infrastructure.adapters.cache import CacheAdapter
from weasel.infrastructure.adapters.cashews.cache import CacheCashewsAdapter
from weasel.infrastructure.adapters.hash import HashAdapter
from weasel.infrastructure.adapters.metrics import MetricsAdapter
from weasel.infrastructure.adapters.mutation_tree import MutationTreeAdapter
from weasel.infrastructure.adapters.sealer import SealerAdapter
from weasel.infrastructure.estimators.damerau_levenshtein import DamerauLevenshteinEstimator
from weasel.infrastructure.estimators.jaro_winkler import JaroWinklerEstimator
from weasel.infrastructure.estimators.levenshtein import LevenshteinEstimator
from weasel.infrastructure.git.bitbucket import BitbucketAdapter
from weasel.infrastructure.git.github import GitHubAdapter
from weasel.infrastructure.languages.java import JavaLanguage
from weasel.infrastructure.languages.python import PythonLanguage
from weasel.infrastructure.languages.sql import SQLLanguage
from weasel.infrastructure.languages.starlark import StarlarkLanguage
from weasel.infrastructure.mutations.java import java001
from weasel.infrastructure.mutations.python import py001, py002, py003, py004, py005, py006
from weasel.infrastructure.mutations.starlark import bzl001, bzl002, bzl003, bzl004, bzl005
from weasel.settings.cache import CacheSettings
from weasel.settings.estimator import EstimatorSettings
from weasel.settings.mutation_tree import MutationTreeSettings
from weasel.settings.retries import RetriesSettings
from weasel.settings.service import ServiceSettings
from weasel.settings.system import SystemSettings


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.git import GitInterface
    from weasel.domain.services.interfaces.hash import HashInterface
    from weasel.domain.services.interfaces.language import LanguageInterface
    from weasel.domain.services.interfaces.metrics import MetricsInterface
    from weasel.domain.services.interfaces.mutation import MutationInterface
    from weasel.domain.services.interfaces.mutation_tree import MutationTreeInterface
    from weasel.domain.services.interfaces.sealer import SealerInterface


class WeaselContainer(DeclarativeContainer):
    """The dependency injection container."""

    service_settings: Provider["ServiceSettings"] = Singleton(ServiceSettings)

    cache_settings: Provider["CacheSettings"] = Singleton(
        CacheSettings, directory=service_settings.provided.cache_directory
    )
    estimator_settings: Provider["EstimatorSettings"] = Singleton(EstimatorSettings)
    mutation_tree_settings: Provider["MutationTreeSettings"] = Singleton(MutationTreeSettings)
    retries_settings: Provider["RetriesSettings"] = Singleton(RetriesSettings)
    system_settings: Provider["SystemSettings"] = Singleton(SystemSettings)

    id_factory: Provider[UUID] = Factory(uuid4)

    cache_cashews_adapter: Provider["CacheCashewsAdapter"] = Singleton(
        CacheCashewsAdapter, _settings=cache_settings.provided
    )

    cache_adapter: Provider["CacheAdapter"] = Singleton(
        CacheAdapter, _cashews=cache_cashews_adapter.provided
    )
    hash_adapter: Provider["HashInterface"] = Singleton(
        HashAdapter, _max_threads=system_settings.provided.max_workers
    )
    metrics_adapter: Provider["MetricsInterface"] = Singleton(
        MetricsAdapter, _precision=service_settings.provided.precision
    )
    sealer_adapter: Provider["SealerInterface"] = Singleton(
        SealerAdapter,
        _data_dir=service_settings.provided.data_directory,
        _id_factory=id_factory.provider,
    )

    bitbucket_adapter: Provider["GitInterface"] = Singleton(
        BitbucketAdapter, _cache=cache_adapter.provided
    )
    github_adapter: Provider["GitInterface"] = Singleton(
        GitHubAdapter, _cache=cache_adapter.provided
    )

    java_language: Provider["LanguageInterface"] = Singleton(JavaLanguage)
    python_language: Provider["LanguageInterface"] = Singleton(PythonLanguage)
    sql_language: Provider["LanguageInterface"] = Singleton(SQLLanguage)
    starlark_language: Provider["LanguageInterface"] = Singleton(StarlarkLanguage)

    languages: Provider[list["LanguageInterface"]] = List(
        java_language.provided,
        python_language.provided,
        sql_language.provided,
        starlark_language.provided,
    )

    damerau_levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(
        DamerauLevenshteinEstimator,
        _cache=cache_adapter.provided,
        _hash=hash_adapter.provided,
        _precision=service_settings.provided.precision,
    )
    jaro_winkler_estimator: Provider["EstimatorInterface"] = Singleton(
        JaroWinklerEstimator,
        _cache=cache_adapter.provided,
        _hash=hash_adapter.provided,
        _precision=service_settings.provided.precision,
    )
    levenshtein_estimator: Provider["EstimatorInterface"] = Singleton(
        LevenshteinEstimator,
        _cache=cache_adapter.provided,
        _hash=hash_adapter.provided,
        _precision=service_settings.provided.precision,
    )

    estimator: Provider["EstimatorInterface"] = Selector(
        estimator_settings.provided.type,
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

    java_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=java_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    python_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=python_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    starlark_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=starlark_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    sql_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator.provided,
        _mutations=sql_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )

    mutation_trees: Provider[dict[LanguageType, "MutationTreeInterface"]] = Dict(
        java=java_mutation_tree.provided,
        python=python_mutation_tree.provided,
        starlark=starlark_mutation_tree.provided,
        sql=sql_mutation_tree.provided,
    )

    scanner: Provider["ScannerService"] = Singleton(
        ScannerService,
        _bitbucket=bitbucket_adapter.provided,
        _concurrency=system_settings.provided.max_workers,
        _estimator=estimator.provided,
        _github=github_adapter.provided,
        _languages=languages.provided,
        _metrics=metrics_adapter.provided,
        _mutation_trees=mutation_trees.provided,
        _sealer=sealer_adapter.provided,
    )


WEASEL_CONTAINER = WeaselContainer()
