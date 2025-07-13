from typing import Any

import pytest

from pyagentai.utils.method_registrar_mixin import _MethodRegistrarMixin


class BaseClass(_MethodRegistrarMixin):
    """A base class for testing."""


async def sample_method(_self: Any) -> str:
    """A sample async method for registration."""
    return "sample"


async def another_method(_self: Any) -> str:
    """Another sample async method."""
    return "another"


def test_register_method() -> None:
    """Test that a method can be registered."""

    class TestClass(BaseClass):
        """A test class."""

    TestClass.register(sample_method)
    assert hasattr(TestClass, "sample_method")
    assert "sample_method" in TestClass._registered
    assert TestClass._registered["sample_method"] == sample_method


def test_register_with_custom_name() -> None:
    """Test that a method can be registered with a custom name."""

    class TestClass(BaseClass):
        """A test class."""

    TestClass.register(sample_method, name="custom_name")
    assert hasattr(TestClass, "custom_name")
    assert not hasattr(TestClass, "sample_method")
    assert "custom_name" in TestClass._registered
    assert TestClass._registered["custom_name"] == sample_method


def test_register_duplicate_method_raises_error() -> None:
    """Test that registering a method with a duplicate name raises an error."""

    class TestClass(BaseClass):
        """A test class."""

    TestClass.register(sample_method)
    with pytest.raises(
        AttributeError, match="Method 'sample_method' already exists"
    ):
        TestClass.register(another_method, name="sample_method")


def test_register_on_subclass_does_not_affect_base() -> None:
    """Test that registering a method on a subclass doesn't affect the base."""

    class SubClass(BaseClass):
        """A subclass of the base class."""

    SubClass.register(sample_method)
    assert hasattr(SubClass, "sample_method")
    assert not hasattr(BaseClass, "sample_method")
    assert "sample_method" in SubClass._registered
    assert "sample_method" not in BaseClass._registered


@pytest.mark.asyncio()
async def test_registered_method_is_callable() -> None:
    """Test that a registered method can be called."""

    class TestClass(BaseClass):
        """A test class."""

    TestClass.register(sample_method)
    instance = TestClass()
    result = await instance.sample_method()
    assert result == "sample"


def test_subclasses_have_independent_registries() -> None:
    """Test that different subclasses have independent method registries."""

    class SubClass1(BaseClass):
        """A subclass of the base class."""

    class SubClass2(BaseClass):
        """A subclass of the base class."""

    SubClass1.register(sample_method)
    SubClass2.register(another_method)

    assert hasattr(SubClass1, "sample_method")
    assert not hasattr(SubClass1, "another_method")

    assert hasattr(SubClass2, "another_method")
    assert not hasattr(SubClass2, "sample_method")


def test_multiple_inheritance() -> None:
    """Test that the mixin works with multiple inheritance."""

    class AnotherMixin:
        """A mixin for testing multiple inheritance."""

        def another_feature(self) -> str:
            return "feature"

    class CombinedClass(BaseClass, AnotherMixin):
        pass

    CombinedClass.register(sample_method)
    instance = CombinedClass()

    assert hasattr(instance, "sample_method")
    assert hasattr(instance, "another_feature")
    assert instance.another_feature() == "feature"


def test_registering_non_callable_raises_error() -> None:
    """Test that registering a non-callable raises an AttributeError."""

    class TestClass(BaseClass):
        pass

    with pytest.raises(AttributeError):
        # We need to ignore the type checker here as
        # we are intentionally passing an invalid type.
        TestClass.register("not a function")  # type: ignore
