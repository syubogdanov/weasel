from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory, List, Provider, Singleton

from weasel.domain.services.matcher import MatcherService
from weasel.domain.services.scanner import ScannerService
from weasel.domain.types.language import LanguageType
from weasel.infrastructure.adapters.api.bitbucket import BitbucketAPIAdapter
from weasel.infrastructure.adapters.api.github import GitHubAPIAdapter
from weasel.infrastructure.adapters.cache import CacheAdapter
from weasel.infrastructure.adapters.cashews.cache import CacheCashewsAdapter
from weasel.infrastructure.adapters.estimator import EstimatorAdapter
from weasel.infrastructure.adapters.metrics import MetricsAdapter
from weasel.infrastructure.adapters.mutation_tree import MutationTreeAdapter
from weasel.infrastructure.adapters.sealer import SealerAdapter
from weasel.infrastructure.git.bitbucket import BitbucketAdapter
from weasel.infrastructure.git.github import GitHubAdapter
from weasel.infrastructure.languages.java import JavaLanguage
from weasel.infrastructure.languages.python import PythonLanguage
from weasel.infrastructure.languages.sql import SQLLanguage
from weasel.infrastructure.languages.starlark import StarlarkLanguage
from weasel.infrastructure.mutations.java import java001
from weasel.infrastructure.mutations.python import py001, py002, py003, py004, py005, py006
from weasel.infrastructure.mutations.sql import (
    sql001,
    sql002,
    sql003,
    sql004,
    sql005,
    sql006,
    sql007,
    sql008,
    sql009,
    sql010,
    sql011,
    sql012,
    sql013,
    sql014,
)
from weasel.infrastructure.mutations.starlark import bzl001, bzl002, bzl003, bzl004, bzl005
from weasel.settings.cache import CacheSettings
from weasel.settings.external_api import ExternalAPISettings
from weasel.settings.mutation_tree import MutationTreeSettings
from weasel.settings.retries import RetriesSettings
from weasel.settings.service import ServiceSettings


if TYPE_CHECKING:
    from weasel.domain.services.interfaces.estimator import EstimatorInterface
    from weasel.domain.services.interfaces.git import GitInterface
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
    external_api_settings: Provider["ExternalAPISettings"] = Singleton(ExternalAPISettings)
    mutation_tree_settings: Provider["MutationTreeSettings"] = Singleton(MutationTreeSettings)
    retries_settings: Provider["RetriesSettings"] = Singleton(RetriesSettings)

    id_factory: Provider[UUID] = Factory(uuid4)

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

    cache_cashews_adapter: Provider["CacheCashewsAdapter"] = Singleton(
        CacheCashewsAdapter, _settings=cache_settings.provided
    )

    cache_adapter: Provider["CacheAdapter"] = Singleton(
        CacheAdapter, _cashews=cache_cashews_adapter.provided
    )
    metrics_adapter: Provider["MetricsInterface"] = Singleton(
        MetricsAdapter, _precision=service_settings.provided.precision
    )
    sealer_adapter: Provider["SealerInterface"] = Singleton(
        SealerAdapter,
        _data_dir=service_settings.provided.data_directory,
        _id_factory=id_factory.provider,
        _languages=languages.provided,
    )

    bitbucket_api_adapter: Provider["BitbucketAPIAdapter"] = Singleton(
        BitbucketAPIAdapter,
        _api_url=external_api_settings.provided.bitbucket_api_url,
        _connect_timeout=external_api_settings.provided.bitbucket_connect_timeout,
        _data_dir=service_settings.provided.data_directory,
        _id_factory=id_factory.provider,
    )
    github_api_adapter: Provider["GitHubAPIAdapter"] = Singleton(
        GitHubAPIAdapter,
        _api_url=external_api_settings.provided.github_api_url,
        _connect_timeout=external_api_settings.provided.github_connect_timeout,
        _data_dir=service_settings.provided.data_directory,
        _id_factory=id_factory.provider,
    )

    bitbucket_adapter: Provider["GitInterface"] = Singleton(
        BitbucketAdapter, _bitbucket=bitbucket_api_adapter.provided, _cache=cache_adapter.provided
    )
    github_adapter: Provider["GitInterface"] = Singleton(
        GitHubAdapter, _cache=cache_adapter.provided, _github=github_api_adapter.provided
    )

    estimator_adapter: Provider["EstimatorInterface"] = Singleton(
        EstimatorAdapter, _precision=service_settings.provided.precision
    )

    bzl001: Provider["MutationInterface"] = Singleton(bzl001.StarlarkMutation)
    bzl002: Provider["MutationInterface"] = Singleton(bzl002.StarlarkMutation)
    bzl003: Provider["MutationInterface"] = Singleton(bzl003.StarlarkMutation)
    bzl004: Provider["MutationInterface"] = Singleton(bzl004.StarlarkMutation)
    bzl005: Provider["MutationInterface"] = Singleton(
        bzl005.StarlarkMutation, _estimator=estimator_adapter.provided
    )

    java001: Provider["MutationInterface"] = Singleton(java001.JavaMutation)

    py001: Provider["MutationInterface"] = Singleton(py001.PythonMutation)
    py002: Provider["MutationInterface"] = Singleton(py002.PythonMutation)
    py003: Provider["MutationInterface"] = Singleton(py003.PythonMutation)
    py004: Provider["MutationInterface"] = Singleton(py004.PythonMutation)
    py005: Provider["MutationInterface"] = Singleton(py005.PythonMutation)
    py006: Provider["MutationInterface"] = Singleton(
        py006.PythonMutation, _estimator=estimator_adapter.provided
    )

    sql001: Provider["MutationInterface"] = Singleton(sql001.SQLMutation)
    sql002: Provider["MutationInterface"] = Singleton(sql002.SQLMutation)
    sql003: Provider["MutationInterface"] = Singleton(sql003.SQLMutation)
    sql004: Provider["MutationInterface"] = Singleton(sql004.SQLMutation)
    sql005: Provider["MutationInterface"] = Singleton(sql005.SQLMutation)
    sql006: Provider["MutationInterface"] = Singleton(sql006.SQLMutation)
    sql007: Provider["MutationInterface"] = Singleton(sql007.SQLMutation)
    sql008: Provider["MutationInterface"] = Singleton(sql008.SQLMutation)
    sql009: Provider["MutationInterface"] = Singleton(sql009.SQLMutation)
    sql010: Provider["MutationInterface"] = Singleton(sql010.SQLMutation)
    sql011: Provider["MutationInterface"] = Singleton(sql011.SQLMutation)
    sql012: Provider["MutationInterface"] = Singleton(sql012.SQLMutation)
    sql013: Provider["MutationInterface"] = Singleton(sql013.SQLMutation)
    sql014: Provider["MutationInterface"] = Singleton(
        sql014.SQLMutation, _estimator=estimator_adapter.provided
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
    sql_mutations: Provider[list["MutationInterface"]] = List(
        sql001.provided,
        sql002.provided,
        sql003.provided,
        sql004.provided,
        sql005.provided,
        sql006.provided,
        sql007.provided,
        sql008.provided,
        sql009.provided,
        sql010.provided,
        sql011.provided,
        sql012.provided,
        sql013.provided,
        sql014.provided,
    )
    starlark_mutations: Provider[list["MutationInterface"]] = List(
        bzl001.provided, bzl002.provided, bzl003.provided, bzl004.provided, bzl005.provided
    )

    java_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator_adapter.provided,
        _mutations=java_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    python_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator_adapter.provided,
        _mutations=python_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    sql_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator_adapter.provided,
        _mutations=sql_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )
    starlark_mutation_tree: Provider["MutationTreeInterface"] = Singleton(
        MutationTreeAdapter,
        _degree_of_freedom=mutation_tree_settings.provided.degree_of_freedom,
        _depth=mutation_tree_settings.provided.depth,
        _estimator=estimator_adapter.provided,
        _mutations=starlark_mutations.provided,
        _tolerance=mutation_tree_settings.provided.tolerance,
    )

    mutation_trees: Provider[dict[LanguageType, "MutationTreeInterface"]] = Dict(
        java=java_mutation_tree.provided,
        python=python_mutation_tree.provided,
        starlark=starlark_mutation_tree.provided,
        sql=sql_mutation_tree.provided,
    )

    matcher_service: Provider["MatcherService"] = Singleton(
        MatcherService,
        _estimator=estimator_adapter.provided,
        _languages=languages.provided,
        _mutation_trees=mutation_trees.provided,
    )
    scanner_service: Provider["ScannerService"] = Singleton(
        ScannerService,
        _bitbucket=bitbucket_adapter.provided,
        _github=github_adapter.provided,
        _matcher=matcher_service.provided,
        _metrics=metrics_adapter.provided,
        _sealer=sealer_adapter.provided,
    )


WEASEL_CONTAINER = WeaselContainer()
