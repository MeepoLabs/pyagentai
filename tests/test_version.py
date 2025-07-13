"""Test version information."""

import re

import pyagentai


def test_version() -> None:
    """Test that version is a valid semver string."""
    assert pyagentai.__version__, "Version should not be empty"
    assert re.match(
        r"^\d+\.\d+\.\d+", pyagentai.__version__
    ), "Version should be a valid semver string"
