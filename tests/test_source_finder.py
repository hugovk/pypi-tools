from __future__ import annotations

import pytest

import source_finder


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            None,
            None,
        ),
        (
            "https://github.com/agronholm/pythonfutures",
            "https://github.com/agronholm/pythonfutures",
        ),
        (
            "https://github.com/protocolbuffers/protobuf/releases",
            "https://github.com/protocolbuffers/protobuf",
        ),
        (
            "https://github.com/uqfoundation/dill/releases/download/dill-0.3.1.1/dill-0.3.1.1.tar.gz",
            "https://github.com/uqfoundation/dill",
        ),
        (
            "https://github.com/tensorflow/tensorflow/tags/",
            "https://github.com/tensorflow/tensorflow",
        ),
    ],
)
def test__normalise_url(test_input, expected):
    # Arrange
    url = test_input

    # Act
    url = source_finder._normalise_url(url)

    # Assert
    assert url == expected
