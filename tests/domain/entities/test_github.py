import pytest

from pydantic import ValidationError

from weasel.domain.entities.github import GitHubEntity


USER = "user"
REPO = "repo"

BRANCH = "branch"
COMMIT = "dcc54ba2eec5bfb73737fcd6722e15c4d28be358"
TAG = "tag"


class TestGitHubEntity:
    """Test the *GitHub* entity."""

    @pytest.mark.parametrize("user", ["", "user-", "some--user", "some__user", "some.user"])
    def test__entity__user(self, user: str) -> None:
        """Test the entity. Case: invalid user."""
        with pytest.raises(ValidationError):
            GitHubEntity(user=user, repo=REPO)

    @pytest.mark.parametrize("repo", ["", "repo-", "some--repo", "some__repo", "some.repo"])
    def test__entity__repo(self, repo: str) -> None:
        """Test the entity. Case: invalid repo."""
        with pytest.raises(ValidationError):
            GitHubEntity(user=USER, repo=repo)

    @pytest.mark.parametrize("branch", ["", "/branch", "branch/", "branch.lock", "@{branch}"])
    def test__entity__branch(self, branch: str) -> None:
        """Test the entity. Case: invalid branch."""
        with pytest.raises(ValidationError):
            GitHubEntity(user=USER, repo=REPO, branch=branch)

    @pytest.mark.parametrize("commit", ["", "commit", "23042003"])
    def test__entity__commit(self, commit: str) -> None:
        """Test the entity. Case: invalid commit."""
        with pytest.raises(ValidationError):
            GitHubEntity(user=USER, repo=REPO, commit=commit)

    @pytest.mark.parametrize("tag", ["", "/tag", "tag/", "tag.lock", "@{tag}"])
    def test__entity__tag(self, tag: str) -> None:
        """Test the entity. Case: invalid tag."""
        with pytest.raises(ValidationError):
            GitHubEntity(user=USER, repo=REPO, tag=tag)

    def test__entity__branch_and_commit(self) -> None:
        """Test the entity. Case: both branch and commit provided."""
        with pytest.raises(ValidationError, match="Both branch and commit provided"):
            GitHubEntity(user=USER, repo=REPO, branch=BRANCH, commit=COMMIT)

    def test__entity__branch_and_tag(self) -> None:
        """Test the entity. Case: both branch and tag provided."""
        with pytest.raises(ValidationError, match="Both branch and tag provided"):
            GitHubEntity(user=USER, repo=REPO, branch=BRANCH, tag=TAG)

    def test__entity__commit_and_tag(self) -> None:
        """Test the entity. Case: both commit and tag provided."""
        with pytest.raises(ValidationError, match="Both commit and tag provided"):
            GitHubEntity(user=USER, repo=REPO, commit=COMMIT, tag=TAG)

    def test__entity__branch_and_commit_and_tag(self) -> None:
        """Test the entity. Case: all three branch, commit and tag provided."""
        with pytest.raises(ValidationError, match="All three branch, commit and tag provided"):
            GitHubEntity(user=USER, repo=REPO, branch=BRANCH, commit=COMMIT, tag=TAG)
