from autogen_agentai.types.agent_info import AgentInfo
from autogen_agentai.utils.client import AgentAIClient


@AgentAIClient.register
async def list_agents(
    self: AgentAIClient,
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
    agents_data: list[dict] = response_data.get("list", [])
    all_agents = [
        AgentInfo.model_validate(agent_data) for agent_data in agents_data
    ]

    # Apply category filter if specified, using tags field
    filtered_agents = all_agents
    if category:
        filtered_agents = [
            agent
            for agent in filtered_agents
            if agent.tags and category in agent.tags
        ]
        await self._logger.debug(
            f"Filtered to {len(filtered_agents)} agents with "
            f"category '{category}'"
        )

    # Apply pagination in memory
    start_idx = min(offset, len(filtered_agents))
    end_idx = min(start_idx + limit, len(filtered_agents))
    paginated_agents = filtered_agents[start_idx:end_idx]
    await self._logger.debug(
        f"Returning {len(paginated_agents)} agents "
        f"(offset: {offset}, limit: {limit})"
    )

    return paginated_agents
