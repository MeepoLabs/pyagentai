from unittest.mock import AsyncMock, patch

import httpx
import pytest

from pyagentai.client import AgentAIClient


@pytest.mark.asyncio()
async def test_client_close_idempotent(client: AgentAIClient) -> None:
    """Test that calling close() multiple times on the client is safe."""
    assert client._http_client is not None

    # First close
    with patch.object(
        client._http_client, "aclose", new_callable=AsyncMock
    ) as mock_aclose:
        await client.close()
        mock_aclose.assert_awaited_once()

    # After the first close, the http_client should be None
    assert client._http_client is None

    # Calling close again should be safe and not raise an error
    await client.close()

    # The http_client should remain None
    assert client._http_client is None


@pytest.mark.asyncio()
async def test_client_reinitialization_after_close() -> None:
    """
    Test that the client and its http_client can be re-initialized after close.
    """
    client = AgentAIClient(api_key="test_key")
    original_http_client = client._http_client
    assert original_http_client is not None

    # Close the client
    await client.close()
    assert client._http_client is None

    # A new request should create a new http_client
    with patch("httpx.AsyncClient") as mock_async_client:
        new_mock_instance = AsyncMock()
        new_mock_instance.request = AsyncMock(
            return_value=httpx.Response(200, json={})
        )
        mock_async_client.return_value = new_mock_instance

        # This call will trigger _initialize_client
        client._initialize_client()
        new_http_client = client._http_client

        assert new_http_client is not None
        assert new_http_client is not original_http_client
