import pytest

import source_finder


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "https://github.com/agronholm/pythonfutures",
            "https://github.com/agronholm/pythonfutures",
        ),
        (
            "https://github.com/protocolbuffers/protobuf/releases",
            "https://github.com/protocolbuffers/protobuf",
        ),
        (
            "https://github.com/uqfoundation/dill/releases/download/dill-0.3.1.1/dill-0.3.1.1.tar.gz",  # noqa: E501
            "https://github.com/uqfoundation/dill",
        ),
    ],
)
def test_normalise_url(test_input, expected):
    # Arrange
    url = test_input

    # Act
    url = source_finder.normalise_url(url)

    # Assert
    assert url == expected
