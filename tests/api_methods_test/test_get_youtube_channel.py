import re
from unittest.mock import AsyncMock

import httpx
import pytest
from _pytest.monkeypatch import MonkeyPatch

from pyagentai.client import AgentAIClient


def test_get_youtube_channel_is_registered(client: AgentAIClient) -> None:
    """Test that get_youtube_channel is a registered method."""
    assert hasattr(client, "get_youtube_channel")
    assert callable(client.get_youtube_channel)


@pytest.mark.asyncio()
async def test_get_youtube_channel_success(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests successful retrieval of YouTube channel data."""
    channel_url = "https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw"
    mock_response_data = {
        "response": {
            "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
            "title": "Test Channel",
            "videos": [],
        }
    }

    mock_response = httpx.Response(
        200,
        json=mock_response_data,
    )
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    channel_info = await client.get_youtube_channel(url=channel_url)

    mock_make_request.assert_awaited_once()
    assert channel_info == mock_response_data["response"]

    call_args = mock_make_request.call_args
    assert call_args.kwargs["data"]["url"] == channel_url
    assert (
        call_args.kwargs["endpoint"]
        == client.config.endpoints.get_youtube_channel
    )


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "invalid_url",
    [
        "not a url",
        "htp://invalid-scheme.com",
        "youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw",
        "",
    ],
)
async def test_get_youtube_channel_invalid_url(
    client: AgentAIClient, invalid_url: str
) -> None:
    """Tests that get_youtube_channel raises ValueError for invalid URLs."""
    expected_error = re.escape(f"Invalid URL provided: '{invalid_url}'")

    with pytest.raises(ValueError, match=expected_error):
        await client.get_youtube_channel(url=invalid_url)


@pytest.mark.asyncio()
async def test_get_youtube_channel_api_empty_response(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests handling of an empty but successful API response."""
    channel_url = "https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw"
    mock_response_data = {"response": {}}

    mock_response = httpx.Response(
        200,
        json=mock_response_data,
    )
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    channel_info = await client.get_youtube_channel(url=channel_url)

    assert channel_info == {}


@pytest.mark.asyncio()
async def test_get_youtube_channel_api_no_response_key(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests handling of an API response without the 'response' key."""
    channel_url = "https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw"
    mock_response_data = {"other_key": "some_data"}

    mock_response = httpx.Response(
        200,
        json=mock_response_data,
    )
    mock_make_request = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client, "_make_request", mock_make_request)

    channel_info = await client.get_youtube_channel(url=channel_url)

    assert channel_info == {}
