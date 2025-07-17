import re
from unittest.mock import AsyncMock

import httpx
import pytest
from pytest import MonkeyPatch  # noqa: PT013

from pyagentai.client import AgentAIClient


def test_get_youtube_transcript_is_registered(client: AgentAIClient) -> None:
    """Test that get_youtube_transcript is a registered method."""
    assert hasattr(client, "get_youtube_transcript")
    assert callable(client.get_youtube_transcript)


@pytest.mark.asyncio()
async def test_get_youtube_transcript_success(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests successful retrieval of a YouTube transcript."""
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    expected_transcript = "Never gonna give you up..."
    expected_metadata = {"duration": 212, "title": "Official Music Video"}

    json_payload = {
        "response": expected_transcript,
        "metadata": expected_metadata,
    }
    mock_response = httpx.Response(200, json=json_payload)
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    transcript, metadata = await client.get_youtube_transcript(url=video_url)

    assert transcript == expected_transcript
    assert metadata == expected_metadata

    client._make_request.assert_awaited_once()
    _, kwargs = client._make_request.call_args
    assert kwargs["data"]["url"] == video_url


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "invalid_url",
    [
        "not a url",
        "www.youtube.com/watch?v=dQw4w9WgXcQ",  # Missing scheme
        "ftp://youtube.com/watch?v=dQw4w9WgXcQ",  # Invalid scheme
        "https://",  # Missing domain
    ],
)
async def test_get_youtube_transcript_invalid_url(
    client: AgentAIClient, invalid_url: str
) -> None:
    """Tests that get_youtube_transcript raises ValueError for invalid URLs."""
    # We must escape the URL as it can contain special regex characters
    escaped_url = re.escape(invalid_url)
    match_str = f"Invalid URL provided: '{escaped_url}'"
    with pytest.raises(ValueError, match=match_str):
        await client.get_youtube_transcript(url=invalid_url)


@pytest.mark.asyncio()
async def test_get_youtube_transcript_api_empty_response(
    client: AgentAIClient, monkeypatch: MonkeyPatch
) -> None:
    """Tests handling of an empty but successful API response."""
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    mock_response = httpx.Response(200, json={})  # Empty JSON
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    transcript, metadata = await client.get_youtube_transcript(url=video_url)

    assert transcript == ""
    assert metadata == {}
