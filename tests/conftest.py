import pytest

from pyagentai.client import AgentAIClient
from pyagentai.types.url_endpoint import (
    Endpoint,
    EndpointParameter,
    ParameterType,
    RequestMethod,
    UrlType,
)


@pytest.fixture()
def client() -> AgentAIClient:
    """Provides a client instance for each test."""
    return AgentAIClient(api_key="test_key")


@pytest.fixture()
def mock_endpoint() -> Endpoint:
    """Provides a mock Endpoint for testing."""
    return Endpoint(
        url="/test",
        method=RequestMethod.GET,
        url_type=UrlType.API,
        query_parameters=[
            EndpointParameter(
                name="required_param",
                param_type=ParameterType.STRING,
                required=True,
            )
        ],
        body_parameters=[],
        requires_auth=True,
    )


@pytest.fixture()
def sample_agent_info() -> dict:
    """Provides a dictionary representing a valid AgentInfo object."""
    return {
        "agent_id": "agent_abc123",
        "agent_id_human": "my-cool-agent",
        "name": "My Cool Agent",
        "description": "This is a test agent.",
        "tags": ["testing", "example"],
        "price": 0,
        "approximate_time": 10,
        "type": "studio",
        "reviews_count": 5,
        "reviews_score": 4.5,
        "invoke_agent_input": {
            "type": "function",
            "function": {
                "name": "mock_function",
                "description": "A mock function for testing",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The user's prompt",
                        }
                    },
                    "required": ["prompt"],
                    "additionalProperties": False,
                },
            },
        },
    }
