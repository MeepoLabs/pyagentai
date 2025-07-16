from unittest.mock import AsyncMock

import httpx
import pytest
from pytest import MonkeyPatch  # noqa: PT013

from pyagentai.client import AgentAIClient


def test_grab_web_text_method_is_registered(client: AgentAIClient) -> None:
    """Test that the grab_web_text method is registered on the client."""
    assert hasattr(client, "grab_web_text")
    assert callable(client.grab_web_text)


@pytest.fixture()
def mock_grab_text_response() -> dict:
    """Provides a mock API response for the grab_web_text endpoint."""
    return {
        "response": "This is the scraped text from the web page.",
        "metadata": {"url": "https://example.com", "title": "Example Domain"},
    }


@pytest.mark.asyncio()
async def test_grab_web_text_calls_make_request_correctly(
    client: AgentAIClient,
    mock_grab_text_response: dict,
    monkeypatch: MonkeyPatch,
) -> None:
    """
    Test that grab_web_text processes arguments and calls
    _make_request correctly.
    """
    mock_response = httpx.Response(200, json=mock_grab_text_response)
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    await client.grab_web_text(url=" https://example.com ", mode=" CRAWL ")

    client._make_request.assert_awaited_once()
    _, kwargs = client._make_request.call_args
    data = kwargs.get("data", {})

    assert data.get("url") == "https://example.com"
    assert data.get("mode") == "crawl"  # Should be lowercased


@pytest.mark.asyncio()
async def test_grab_web_text_parses_response(
    client: AgentAIClient,
    mock_grab_text_response: dict,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that grab_web_text correctly parses the JSON response."""
    mock_response = httpx.Response(200, json=mock_grab_text_response)
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    text, metadata = await client.grab_web_text(url="https://example.com")

    assert text == "This is the scraped text from the web page."
    assert metadata == {"url": "https://example.com", "title": "Example Domain"}


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "invalid_url",
    [
        "not-a-url",
        "http://",  # no domain
        "ftp://example.com",  # invalid scheme
        "example.com",  # no scheme
    ],
)
async def test_grab_web_text_with_invalid_url(
    client: AgentAIClient, invalid_url: str
) -> None:
    """Test that grab_web_text raises ValueError for invalid URLs."""
    with pytest.raises(
        ValueError, match=f"Invalid URL provided: '{invalid_url}'"
    ):
        await client.grab_web_text(url=invalid_url)
