from __future__ import annotations

import pytest

import top_repos


@pytest.mark.parametrize(
    "packages, expected_output_packages, expected_changed",
    [
        # Example of repo found and updated
        (
            [
                {"name": "name1", "repo": "https://github.com/repo/1"},
                {"name": "name2", "repo": "https://github.com/repo/2"},
                {"name": "name3", "repo": "https://github.com/repo/3"},
            ],
            [
                {"name": "name1", "repo": "https://github.com/repo/1"},
                {"name": "name2", "repo": "https://github.com/repo/new"},
                {"name": "name3", "repo": "https://github.com/repo/3"},
            ],
            1,
        ),
        # Example of repo not found so not updated
        (
            [
                {"name": "name1", "repo": "https://github.com/repo/1"},
                {"name": "name3", "repo": "https://github.com/repo/3"},
            ],
            [
                {"name": "name1", "repo": "https://github.com/repo/1"},
                {"name": "name3", "repo": "https://github.com/repo/3"},
            ],
            0,
        ),
    ],
)
def test_update_existing(packages, expected_output_packages, expected_changed):
    # Arrange
    name_to_find = "name2"
    new_repo = "https://github.com/repo/new"

    # Act
    output_changed = top_repos.update_existing(packages, name_to_find, new_repo)

    # Assert
    assert packages == expected_output_packages
    assert output_changed == output_changed
