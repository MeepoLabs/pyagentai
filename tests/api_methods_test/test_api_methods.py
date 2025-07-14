from unittest.mock import AsyncMock

import httpx
import pytest

from pyagentai.client import AgentAIClient
from pyagentai.types.agent_info import AgentInfo


@pytest.fixture()
def mock_agents_response(sample_agent_info: dict) -> dict:
    """Provides a mock API response containing a list of agents."""
    # A minimal but valid structure for invoke_agent_input
    invoke_input = sample_agent_info["invoke_agent_input"]
    return {
        "response": [
            {
                "agent_id": "1",
                "name": "Agent 1",
                "slug": "agent-1",
                "description": "Desc 1",
                "tags": ["a"],
                "invoke_agent_input": invoke_input,
            },
            {
                "agent_id": "2",
                "name": "Agent 2",
                "slug": "agent-2",
                "description": "Desc 2",
                "tags": ["b"],
                "invoke_agent_input": invoke_input,
            },
            {
                "agent_id": "3",
                "name": "Agent 3",
                "slug": "agent-3",
                "description": "Desc 3",
                "tags": ["a", "c"],
                "invoke_agent_input": invoke_input,
            },
            {
                "agent_id": "4",
                "name": "Agent 4",
                "slug": "agent-4",
                "description": "Desc 4",
                "tags": ["d"],
                "invoke_agent_input": invoke_input,
            },
            {
                "agent_id": "5",
                "name": "Agent 5",
                "slug": "agent-5",
                "description": "Desc 5",
                "tags": ["e"],
                "invoke_agent_input": invoke_input,
            },
        ]
    }


def test_find_agents_method_is_registered(client: AgentAIClient) -> None:
    """Test that the find_agents method is registered on the client."""
    assert hasattr(client, "find_agents")
    assert callable(client.find_agents)


def test_mock_agent_response_structure(mock_agents_response: dict) -> None:
    """
    Validate that the mock agent response fixture conforms to the
    AgentInfo schema.
    """
    agents_data = mock_agents_response.get("response", [])
    assert isinstance(agents_data, list)
    # This will raise a ValidationError if any item is invalid
    for agent_data in agents_data:
        AgentInfo.model_validate(agent_data)


@pytest.mark.asyncio()
async def test_find_agents_calls_make_request_correctly(
    client: AgentAIClient, mock_agents_response: dict
) -> None:
    """
    Test that find_agents processes arguments and calls
    _make_request correctly.
    """
    mock_response = httpx.Response(200, json=mock_agents_response)
    client._make_request = AsyncMock(return_value=mock_response)

    await client.find_agents(status=" public ", tag="a", query="search term")

    client._make_request.assert_awaited_once()
    _, kwargs = client._make_request.call_args
    data = kwargs.get("data", {})

    assert data.get("status") == "public"
    assert data.get("tag") == "a"
    assert data.get("query") == "search term"
    assert "intent" not in data


@pytest.mark.asyncio()
async def test_find_agents_parses_response(
    client: AgentAIClient, mock_agents_response: dict
) -> None:
    """
    Test that find_agents correctly parses the JSON response into
    AgentInfo objects.
    """
    mock_response = httpx.Response(200, json=mock_agents_response)
    client._make_request = AsyncMock(return_value=mock_response)

    agents = await client.find_agents()

    assert isinstance(agents, list)
    assert len(agents) == 5
    assert all(isinstance(agent, AgentInfo) for agent in agents)
    assert agents[0].name == "Agent 1"


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("offset", "limit", "expected_ids"),
    [
        (0, 2, ["1", "2"]),
        (2, 2, ["3", "4"]),
        (4, 2, ["5"]),
        (0, 5, ["1", "2", "3", "4", "5"]),
        (5, 5, []),  # Offset is beyond the list size
        (10, 2, []),  # Offset is way beyond the list size
    ],
)
async def test_find_agents_pagination(
    client: AgentAIClient,
    mock_agents_response: dict,
    offset: int,
    limit: int,
    expected_ids: list[str],
) -> None:
    """Test the in-memory pagination of find_agents."""
    mock_response = httpx.Response(200, json=mock_agents_response)
    client._make_request = AsyncMock(return_value=mock_response)

    paginated_agents = await client.find_agents(offset=offset, limit=limit)

    assert [agent.agent_id for agent in paginated_agents] == expected_ids


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("offset", "limit", "expected_length"),
    [
        (-1, 5, 0),  # Negative offset
        (0, -1, 0),  # Negative limit
        (0, 0, 5),  # Zero limit should return all agents
    ],
)
async def test_find_agents_pagination_edge_cases(
    client: AgentAIClient,
    mock_agents_response: dict,
    offset: int,
    limit: int,
    expected_length: int,
) -> None:
    """Test pagination edge cases like negative or zero values."""
    mock_response = httpx.Response(200, json=mock_agents_response)
    client._make_request = AsyncMock(return_value=mock_response)

    paginated_agents = await client.find_agents(offset=offset, limit=limit)
    assert len(paginated_agents) == expected_length


@pytest.mark.asyncio()
@pytest.mark.parametrize("status_val", [None, ""])
async def test_find_agents_handles_none_and_empty_params(
    client: AgentAIClient, mock_agents_response: dict, status_val: str | None
) -> None:
    """Test that None and empty string parameters are handled correctly."""
    mock_response = httpx.Response(200, json=mock_agents_response)
    client._make_request = AsyncMock(return_value=mock_response)

    await client.find_agents(status=status_val)

    # The `status` parameter should not be in the request data
    # because it's either None or an empty string that gets stripped.
    _, kwargs = client._make_request.call_args
    assert "status" not in kwargs.get("data", {})


@pytest.mark.asyncio()
async def test_find_agents_handles_empty_response(
    client: AgentAIClient,
) -> None:
    """Test find_agents with an empty list of agents in the response."""
    empty_response = {"response": []}
    mock_response = httpx.Response(200, json=empty_response)
    client._make_request = AsyncMock(return_value=mock_response)

    agents = await client.find_agents()

    assert isinstance(agents, list)
    assert len(agents) == 0
