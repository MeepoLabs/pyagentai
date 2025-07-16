from unittest.mock import AsyncMock

import httpx
import pytest
from pytest import MonkeyPatch  # noqa: PT013

from pyagentai.client import AgentAIClient


@pytest.fixture()
def mock_grab_screenshot_response() -> dict:
    """Provides a mock API response for grab_web_screenshot."""
    return {"response": "https://example.com/screenshot.png"}


def test_grab_web_screenshot_is_registered(client: AgentAIClient) -> None:
    """Test that grab_web_screenshot is a registered method."""
    assert hasattr(client, "grab_web_screenshot")
    assert callable(client.grab_web_screenshot)


@pytest.mark.asyncio()
async def test_grab_web_screenshot_calls_make_request_correctly(
    client: AgentAIClient,
    mock_grab_screenshot_response: dict,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that grab_web_screenshot formats the request correctly."""
    mock_response = httpx.Response(200, json=mock_grab_screenshot_response)
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    test_url = "https://valid-url.com"
    test_ttl = 86400
    await client.grab_web_screenshot(url=test_url, ttl_for_screenshot=test_ttl)

    # _make_request should be awaited
    client._make_request.assert_awaited_once()

    # Check that the arguments are correct
    call_args = client._make_request.call_args
    endpoint = client.config.endpoints.grab_web_screenshot
    assert call_args.kwargs["endpoint"] == endpoint
    assert call_args.kwargs["data"]["url"] == test_url
    assert call_args.kwargs["data"]["ttl_for_screenshot"] == test_ttl


@pytest.mark.asyncio()
async def test_grab_web_screenshot_uses_default_ttl(
    client: AgentAIClient,
    mock_grab_screenshot_response: dict,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that grab_web_screenshot uses the default TTL when not provided."""
    mock_response = httpx.Response(200, json=mock_grab_screenshot_response)
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    await client.grab_web_screenshot(url="https://valid-url.com")

    client._make_request.assert_awaited_once()

    call_args = client._make_request.call_args
    assert call_args.kwargs["data"]["ttl_for_screenshot"] == 3600  # Default


@pytest.mark.asyncio()
async def test_grab_web_screenshot_parses_response(
    client: AgentAIClient,
    mock_grab_screenshot_response: dict,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that grab_web_screenshot correctly parses the JSON response."""
    mock_response = httpx.Response(200, json=mock_grab_screenshot_response)
    monkeypatch.setattr(
        client, "_make_request", AsyncMock(return_value=mock_response)
    )

    screenshot_url = await client.grab_web_screenshot(
        url="https://example.com"
    )

    assert screenshot_url == mock_grab_screenshot_response["response"]


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "invalid_url",
    [
        "not a url",
        "example.com",
        "ftp://example.com",
        "",
    ],
)
async def test_grab_web_screenshot_raises_for_invalid_urls(
    client: AgentAIClient, invalid_url: str
) -> None:
    """Test that grab_web_screenshot raises ValueError for invalid URLs."""
    with pytest.raises(
        ValueError, match=f"Invalid URL provided: '{invalid_url}'"
    ):
        await client.grab_web_screenshot(url=invalid_url)
