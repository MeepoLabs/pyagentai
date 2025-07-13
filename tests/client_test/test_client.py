from typing import Any

import httpx
import pytest

from pyagentai.client import AgentAIClient
from pyagentai.config.agentai_config import AgentAIConfig
from pyagentai.types.url_endpoint import (
    Endpoint,
    EndpointParameter,
    ParameterType,
)


def test_client_initialization_with_api_key(client: AgentAIClient) -> None:
    """Test that the client initializes correctly with a direct API key."""
    assert client.config.api_key == "test_key"


def test_client_initialization_with_config() -> None:
    """Test that the client initializes correctly with a config object."""
    config = AgentAIConfig(api_key="config_key")
    client = AgentAIClient(config=config)
    assert client.config.api_key == "config_key"


def test_client_initialization_key_overrides_config() -> None:
    """Test that a direct API key overrides the one in the config."""
    config = AgentAIConfig(api_key="config_key")
    client = AgentAIClient(api_key="override_key", config=config)
    assert client.config.api_key == "override_key"


@pytest.mark.asyncio()
async def test_validate_parameter_valid(client: AgentAIClient) -> None:
    """Test that valid parameters pass validation."""
    param = EndpointParameter(
        name="test_param",
        param_type=ParameterType.STRING,
        required=True,
    )
    validated_value = await client._validate_parameter(param, "valid_string")
    assert validated_value == "valid_string"


@pytest.mark.asyncio()
async def test_validate_parameter_invalid_type(client: AgentAIClient) -> None:
    """Test that a parameter with an invalid type raises a ValueError."""
    param = EndpointParameter(
        name="test_param",
        param_type=ParameterType.INTEGER,
        required=True,
    )
    with pytest.raises(ValueError, match="Invalid type for 'test_param'"):
        await client._validate_parameter(param, "not_an_integer")


@pytest.mark.asyncio()
async def test_validate_parameter_bool_is_not_int(
    client: AgentAIClient
) -> None:
    """Test that a boolean is not considered a valid integer."""
    param = EndpointParameter(
        name="test_param",
        param_type=ParameterType.INTEGER,
        required=True,
    )
    with pytest.raises(ValueError, match="Expected integer, got boolean"):
        await client._validate_parameter(param, True)


@pytest.mark.asyncio()
async def test_validate_parameter_allowed_values(client: AgentAIClient) -> None:
    """Test validation against a list of allowed values."""
    param = EndpointParameter(
        name="test_param",
        param_type=ParameterType.STRING,
        required=True,
        validate_parameter=True,
        allowed_values=["A", "B"],
    )
    assert await client._validate_parameter(param, "A") == "A"
    with pytest.raises(ValueError, match="Invalid value for test_param: 'C'"):
        await client._validate_parameter(param, "C")


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("param_type", "valid_value"),
    [
        (ParameterType.FILE, "/path/to/file.txt"),
        (ParameterType.OBJECT, {"key": "value"}),
        (ParameterType.ARRAY, [1, 2, 3]),
    ],
)
async def test_validate_parameter_other_types(
    client: AgentAIClient, param_type: ParameterType, valid_value: Any
) -> None:
    """Test validation for FILE, OBJECT, and ARRAY types."""
    param = EndpointParameter(name="test", param_type=param_type, required=True)
    assert await client._validate_parameter(param, valid_value) == valid_value


@pytest.mark.asyncio()
async def test_validate_parameter_skipped_when_flag_is_false(
    client: AgentAIClient,
) -> None:
    """Test that validation is skipped if validate_parameter is False."""
    param = EndpointParameter(
        name="test_param",
        param_type=ParameterType.STRING,
        required=True,
        validate_parameter=False,  # Skip validation
        allowed_values=["A", "B"],
    )
    # This value is not in allowed_values, but should pass
    validated_value = await client._validate_parameter(param, "C")
    assert validated_value == "C"


@pytest.mark.asyncio()
async def test_make_request_successful(
    client: AgentAIClient,
    mock_endpoint: Endpoint,
) -> None:
    """Test a successful API request."""

    def mock_response(request: httpx.Request) -> httpx.Response:
        assert "Bearer test_key" in request.headers["Authorization"]
        return httpx.Response(200, json={"status": "ok"})

    transport = httpx.MockTransport(mock_response)
    client._http_client = httpx.AsyncClient(transport=transport)

    response = await client._make_request(
        endpoint=mock_endpoint, data={"required_param": "value"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio()
async def test_make_request_missing_required_param(
    client: AgentAIClient, mock_endpoint: Endpoint
) -> None:
    """Test that a request fails if a required parameter is missing."""
    with pytest.raises(
        ValueError, match="Parameter 'required_param' is required"
    ):
        await client._make_request(endpoint=mock_endpoint, data={})


@pytest.mark.asyncio()
async def test_make_request_http_status_error(
    client: AgentAIClient, mock_endpoint: Endpoint
) -> None:
    """Test that an HTTP status error is handled correctly."""
    transport = httpx.MockTransport(
        lambda req: httpx.Response(500, json={"detail": "Server Error"})
    )
    client._http_client = httpx.AsyncClient(transport=transport)

    with pytest.raises(ValueError, match="HTTP error 500"):
        await client._make_request(
            endpoint=mock_endpoint, data={"required_param": "value"}
        )


@pytest.mark.asyncio()
async def test_make_request_timeout_error(
    client: AgentAIClient, mock_endpoint: Endpoint
) -> None:
    """Test that a timeout error is handled correctly."""

    def raise_timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timeout")

    transport = httpx.MockTransport(raise_timeout)
    client._http_client = httpx.AsyncClient(transport=transport)

    with pytest.raises(ValueError, match="API request timed out"):
        await client._make_request(
            endpoint=mock_endpoint, data={"required_param": "value"}
        )
