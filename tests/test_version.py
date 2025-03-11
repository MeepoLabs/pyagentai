"""Test version information."""

import re

import your_package_name


def test_version() -> None:
    """Test that version is a valid semver string."""
    assert your_package_name.__version__, "Version should not be empty"
    assert re.match(
        r"^\d+\.\d+\.\d+", your_package_name.__version__
    ), "Version should be a valid semver string"
