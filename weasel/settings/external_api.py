from pydantic import BaseModel, NonNegativeFloat


class ExternalAPISettings(BaseModel):
    """The external API settings."""

    # The Bitbucket API URL.
    bitbucket_api_url: str = "https://bitbucket.org/"
    # The Bitbucket API connect timeout.
    bitbucket_connect_timeout: NonNegativeFloat = 5.0

    # The GitHub API URL.
    github_api_url: str = "https://api.github.com/"
    # The GitHub API connect timeout.
    github_connect_timeout: NonNegativeFloat = 5.0
