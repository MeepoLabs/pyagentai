"""Tests for core functionality."""

from autogen_agentai import AgentAIExtension


def test_agent_ai_extension_init() -> None:
    """Test AgentAIExtension initialization."""
    api_key = "test_api_key"
    extension = AgentAIExtension(api_key=api_key)
    assert extension.api_key == api_key
    assert extension.config == {"api_key": api_key}


def test_agent_ai_extension_register() -> None:
    """Test AgentAIExtension register method."""
    extension = AgentAIExtension(api_key="test_api_key")
    # This should not raise an exception
    extension.register(None)


def test_agent_ai_extension_connect() -> None:
    """Test AgentAIExtension connect_to_agentai method."""
    extension = AgentAIExtension(api_key="test_api_key")
    # Method currently returns None as it's a placeholder
    assert extension.connect_to_agentai("test_agent_id") is None
