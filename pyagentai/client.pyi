# pyagentai/client.pyi
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import httpx

from pyagentai.config.agentai_config import AgentAIConfig
from pyagentai.types.agent_info import AgentInfo
from pyagentai.types.url_endpoint import Endpoint

T = TypeVar("T", bound=Callable[..., Awaitable[Any]])

class AgentAIClient:
    """
    Type stub for AgentAIClient.

    This file provides type hints for static analysis tools like mypy and
    for IDEs like VSCode, allowing them to understand the methods that are
    dynamically attached to the client at runtime.
    """

    # --- Statically defined attributes ---
    config: AgentAIConfig
    _logger: Any

    # --- Statically defined methods ---
    def __init__(
        self,
        api_key: str | None = None,
        config: AgentAIConfig | None = None,
    ) -> None: ...
    async def close(self) -> None: ...

    # --- Internal methods used by registered functions ---
    async def _make_request(
        self, endpoint: Endpoint, data: dict[str, Any] | None = None
    ) -> httpx.Response: ...

    # --- Class methods for dynamic registration ---
    @classmethod
    def register(cls, func: T, *, name: str | None = None) -> T: ...

    # --- Dynamically registered methods ---
    # --- Find Agents ---
    async def find_agents(
        self,
        status: str | None = None,
        slug: str | None = None,
        query: str | None = None,
        tag: str | None = None,
        intent: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[AgentInfo]: ...

    # --- Grab Web Text ---
    async def grab_web_text(
        self,
        url: str,
        mode: str = "scrape",
    ) -> tuple[str, dict]: ...

    # --- Grab Web Screenshot ---
    async def grab_web_screenshot(
        self,
        url: str,
        ttl_for_screenshot: int = 3600,
    ) -> str: ...
