import re
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
from pytest import MonkeyPatch  # noqa: PT013

from pyagentai.client import AgentAIClient


def test_get_twitter_users_is_registered(client: AgentAIClient) -> None:
    """Test that get_twitter_users is a registered method."""
    assert hasattr(client, "get_twitter_users")
    assert callable(client.get_twitter_users)


@pytest.mark.asyncio()
async def test_get_twitter_users_success(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests a successful call to get_twitter_users."""
    keywords = "test keywords"
    num_users = 5
    mock_response_data = {"response": ["user1", "user2"]}

    mock_response = httpx.Response(200, json=mock_response_data)
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    users = await client.get_twitter_users(
        keywords=keywords, num_users=num_users
    )

    assert users == mock_response_data["response"]
    mock_make_request.assert_awaited_once()

    _, kwargs = mock_make_request.call_args
    assert kwargs["data"]["keywords"] == keywords
    assert kwargs["data"]["num_users"] == num_users
    assert kwargs["endpoint"] == client.config.endpoints.get_twitter_users


@pytest.mark.asyncio()
async def test_get_twitter_users_default_num_users(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests that the default value for num_users is used correctly."""
    keywords = "test keywords"
    mock_response_data = {"response": ["user1"]}

    mock_response = httpx.Response(200, json=mock_response_data)
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    await client.get_twitter_users(keywords=keywords)

    mock_make_request.assert_awaited_once()
    _, kwargs = mock_make_request.call_args
    assert kwargs["data"]["num_users"] == 1  # Default value


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "invalid_keywords",
    [
        "",
        "   ",
    ],
)
async def test_get_twitter_users_invalid_keywords(
    client: AgentAIClient, invalid_keywords: str
) -> None:
    """Tests that get_twitter_users raises ValueError for invalid keywords."""
    with pytest.raises(ValueError, match="Keywords cannot be empty."):
        await client.get_twitter_users(keywords=invalid_keywords)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "invalid_num_users",
    [0, 2, 101, -5],
)
async def test_get_twitter_users_invalid_num_users(
    client: AgentAIClient, invalid_num_users: int
) -> None:
    """Tests that get_twitter_users raises ValueError for invalid num_users."""
    expected_error = re.escape(
        f"Invalid value for num_users: '{invalid_num_users}'. "
        f"Allowed: [1, 5, 10, 25, 50, 100]"
    )
    with pytest.raises(ValueError, match=expected_error):
        await client.get_twitter_users(
            keywords="valid", num_users=invalid_num_users
        )


@pytest.mark.asyncio()
async def test_get_twitter_users_strips_keywords(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests that keywords are stripped of whitespace."""
    keywords = "  test keywords  "
    stripped_keywords = "test keywords"
    mock_response_data = {"response": ["user1"]}

    mock_response = httpx.Response(200, json=mock_response_data)
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    await client.get_twitter_users(keywords=keywords)

    mock_make_request.assert_awaited_once()
    _, kwargs = mock_make_request.call_args
    assert kwargs["data"]["keywords"] == stripped_keywords


@pytest.mark.asyncio()
async def test_get_twitter_users_api_empty_response(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests handling of an empty list in the API response."""
    mock_response_data: dict[str, Any] = {"response": []}
    mock_response = httpx.Response(200, json=mock_response_data)
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    users = await client.get_twitter_users(keywords="test")
    assert users == []


@pytest.mark.asyncio()
async def test_get_twitter_users_api_no_response_key(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests handling of an API response without the 'response' key."""
    mock_response_data = {"other_key": "some_data"}
    mock_response = httpx.Response(200, json=mock_response_data)
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    users = await client.get_twitter_users(keywords="test")
    assert users == []
