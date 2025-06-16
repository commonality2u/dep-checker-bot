"""Minimal stubs for the ``github`` package used in tests.

These classes mimic the interfaces from the ``PyGithub`` package that are
referenced in the codebase. Only the attributes required by the unit tests are
implemented.
"""


class GithubException(Exception):
    """Simple exception carrying an HTTP status code."""

    def __init__(self, status, data=None, headers=None):
        super().__init__(data)
        self.status = status
        self.data = data
        self.headers = headers


class Github:
    """Placeholder ``Github`` client."""

    def __init__(self, token):
        self.token = token

    # The real ``Github`` class exposes many methods. Tests only rely on
    # ``get_repo`` returning an object with certain attributes, so this method
    # simply raises ``NotImplementedError`` and should be patched in tests.
    def get_repo(self, name):  # pragma: no cover - replaced by mocks in tests
        raise NotImplementedError


class InputGitAuthor:
    """Simple data container for commit author information."""

    def __init__(self, name, email):
        self.name = name
        self.email = email
