from pydantic import BaseModel, Field


class AgentInfo(BaseModel):
    """A data class for storing summarized agent information."""

    agent_id: str = Field(
        ..., description="The unique identifier for the agent."
    )
    name: str = Field(..., description="The name of the agent.")
    description: str | None = Field(
        "", description="A brief description of the agent."
    )
    tags: list[str] = Field([], description="Tags associated with the agent.")
    price: float = Field(
        0.0, description="The price or cost associated with using the agent."
    )
