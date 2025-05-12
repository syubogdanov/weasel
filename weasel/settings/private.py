from pydantic import BaseModel, PositiveInt


class PrivateSettings(BaseModel):
    """The private settings.

    Notes
    -----
    * The settings are not meant to be overridden by environment variables;
    * `pydantic_settings` must not be used.
    """

    # The number of top-scoring mutation branches to explore.
    mutation_tree_degree_of_freedom: PositiveInt = 3
    # The maximum depth of the mutation tree.
    mutation_tree_depth: PositiveInt = 3
