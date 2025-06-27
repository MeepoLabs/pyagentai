"""Client for interacting with agent.ai API."""

import asyncio
from typing import Any

import httpx
import structlog

from autogen_agentai.config.agentai_config import AgentAIConfig
from autogen_agentai.types.agent_info import AgentInfo
from autogen_agentai.types.url_endpoint import Endpoint, UrlType

logger = structlog.get_logger("autogen_agentai.client")


class AgentAIClient:
    """Client for the agent.ai API.

    This client handles authentication and communication with the agent.ai API.

    Attributes:
        config: The configuration for the client.
    """

    def __init__(
        self,
        api_key: str | None = None,
        config: AgentAIConfig | None = None,
    ) -> None:
        """Initialize the agent.ai API client.

        Args:
            api_key: The API key for authenticating with agent.ai.
                If provided, overrides the key in the config.
            config: The configuration for the client.
                If not provided, a default configuration is used.
        """
        if config is None:
            config = AgentAIConfig()
        self.config = config

        if api_key:
            self.config.api_key = api_key

        self._http_client: httpx.AsyncClient | None = None
        self._agent_cache: dict[str, dict[str, Any]] = {}
        self._event_loop = asyncio.get_event_loop()
        self._initialize_client()

    def _initialize_client(self) -> httpx.AsyncClient:
        """Initialize the HTTP client.

        Returns:
            The initialized HTTP client.
        """
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                headers={
                    "Content-Type": "application/json",
                },
                timeout=self.config.timeout,
                http2=True,
            )
            self._event_loop.create_task(
                logger.debug("HTTP client initialized")
            )
        return self._http_client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._http_client is not None and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None

        await logger.debug("HTTP client closed")

    async def _make_request(
        self, endpoint: Endpoint, data: dict[str, Any] | None = None
    ) -> httpx.Response:
        """Make a request to the agent.ai API.

        Args:
            endpoint: The API endpoint to call.
            data: The request body data.
            query_params: The query parameters.

        Returns:
            The httpx response object.

        Raises:
            ValueError: If the request fails.
        """
        if data is None:
            data = {}

        client = self._initialize_client()

        # Determine base URL based on endpoint type
        if endpoint.url_type == UrlType.WEB:
            base_url = self.config.web_url
        else:
            base_url = self.config.api_url

        url = f"{base_url}{endpoint.url}"
        query_params = {}
        body_params = {}

        # Parse query and body parameters from data
        for param in endpoint.query_parameters:
            query_params[param.name] = data.pop(param.name, param.default)

        for param in endpoint.body_parameters:
            body_params[param.name] = data.pop(param.name, param.default)
        body_params.update(data)

        # Parse headers from endpoint
        headers = {}
        headers["Content-Type"] = endpoint.request_content_type
        headers["Accept"] = endpoint.response_content_type

        if endpoint.requires_auth:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        try:
            await logger.debug(f"Making {endpoint.method} request to {url}")
            response = await client.request(
                method=endpoint.method.value,
                url=url,
                params=query_params,
                json=body_params,
                headers=headers,
            )
            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as e:
            error_detail = f"HTTP error {e.response.status_code}"
            try:
                error_json = e.response.json()
                error_detail = f"{error_detail}: {error_json}"
            except Exception as exc:  # noqa: W0718
                # ignore this error
                await logger.debug(f"Error parsing response: {exc}")
            await logger.error(f"API request failed: {error_detail}")
            raise ValueError(f"API request failed: {error_detail}") from e

        except httpx.TimeoutException as e:
            await logger.error(f"API request timed out: {str(e)}")
            raise ValueError("API request timed out") from e

        except httpx.HTTPError as e:
            await logger.error(f"HTTP error: {str(e)}")
            raise ValueError(f"HTTP error: {str(e)}") from e

        except Exception as e:
            await logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}") from e

    async def list_agents(
        self,
        category: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[AgentInfo]:
        """List available agents on agent.ai.

        Args:
            category: Filter agents by category.
            limit: Maximum number of agents to return.
            offset: Offset for pagination.

        Returns:
            List of available agents with their summarized information.
        """
        # Agent.ai uses a simple POST request without parameters
        endpoint = self.config.endpoints.list_agents
        data = {}

        # The api does not filter by category
        # We will filter it in memory
        if category is not None:
            category = category.strip().capitalize()
            data["category"] = category

        response = await self._make_request(
            endpoint=endpoint,
            data=data,
        )
        response_data = response.json()

        # Extract agents from response
        agents_data: list[dict[str, Any]] = response_data.get("list", [])
        all_agents = [
            AgentInfo.model_validate(agent_data) for agent_data in agents_data
        ]
        await logger.debug(f"Retrieved {len(all_agents)} agents from agent.ai")

        # Apply category filter if specified, using tags field
        filtered_agents = all_agents
        if category:
            filtered_agents = [
                agent
                for agent in filtered_agents
                if agent.tags and category in agent.tags
            ]
            await logger.debug(
                f"Filtered to {len(filtered_agents)} agents with "
                f"category '{category}'"
            )

        # Apply pagination in memory
        start_idx = min(offset, len(filtered_agents))
        end_idx = min(start_idx + limit, len(filtered_agents))
        paginated_agents = filtered_agents[start_idx:end_idx]
        await logger.debug(
            f"Returning {len(paginated_agents)} agents "
            f"(offset: {offset}, limit: {limit})"
        )

        return paginated_agents
