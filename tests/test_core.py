"""Tests for core functionality."""

from your_package_name import YourClass, your_function


def test_your_class() -> None:
    """Test YourClass functionality."""
    instance = YourClass(parameter="test")
    result = instance.method()
    assert result == "Operation completed with parameter: test"
    assert instance.parameter == "test"


def test_your_function() -> None:
    """Test your_function functionality."""
    result = your_function("test input")
    assert result["input"] == "test input"
    assert result["processed"] is True
    assert result["result"] == "Processed: test input"
