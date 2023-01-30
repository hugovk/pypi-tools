from __future__ import annotations

import pytest

import repo_checker


@pytest.mark.parametrize(
    "test_input",
    [
        "http://github.com/octocat/Hello-World",
        "http://github.com/octocat/Hello-World/",
        "https://github.com/octocat/Hello-World",
        "https://github.com/octocat/Hello-World.git",
        "https://github.com/octocat/Hello-World.git",
        "https://github.com/octocat/Hello-World/",
    ],
)
def test_repo_url_dir_name(test_input):
    # Arrange
    repo_url = test_input

    # Act
    dir_name = repo_checker.repo_url_dir_name(repo_url)

    # Assert
    assert dir_name == "Hello-World"
