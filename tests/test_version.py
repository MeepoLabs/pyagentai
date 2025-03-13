"""Test version information."""

import re

import autogen_agentai


def test_version() -> None:
    """Test that version is a valid semver string."""
    assert autogen_agentai.__version__, "Version should not be empty"
    assert re.match(
        r"^\d+\.\d+\.\d+", autogen_agentai.__version__
    ), "Version should be a valid semver string"
