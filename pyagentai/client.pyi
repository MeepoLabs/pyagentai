# pyagentai/client.pyi
from typing import Any

from pyagentai.config.agentai_config import AgentAIConfig
from pyagentai.types.agent_info import AgentInfo

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

    # --- Dynamically registered methods ---
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
