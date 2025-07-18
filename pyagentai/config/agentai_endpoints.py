"""Configuration for agent.ai API endpoints."""

from pydantic import BaseModel, Field

from pyagentai.types.url_endpoint import (
    Endpoint,
    EndpointParameter,
    ParameterType,
    RequestMethod,
    UrlType,
)


class AgentAIEndpoints(BaseModel):
    """Endpoints for agent.ai API."""

    find_agents: Endpoint = Field(
        default=Endpoint(
            url="/action/find_agents",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description=(
                "Search and discover agents based on various "
                "criteria including status, tags, and search terms."
            ),
            requires_auth=True,
            response_content_type="application/json",
            request_content_type="application/json",
            body_parameters=[
                EndpointParameter(
                    name="status",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="Filter agents by their visibility status.",
                    allowed_values=["any", "public", "private"],
                    validate_parameter=True,
                ),
                EndpointParameter(
                    name="slug",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="Filter agents by their human readable slug.",
                    validate_parameter=False,
                ),
                EndpointParameter(
                    name="query",
                    param_type=ParameterType.STRING,
                    required=False,
                    description=(
                        "Text to search for in agent names and descriptions."
                    ),
                    validate_parameter=False,
                ),
                EndpointParameter(
                    name="tag",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="Filter agents by specific tag.",
                    validate_parameter=False,
                ),
                EndpointParameter(
                    name="intent",
                    param_type=ParameterType.STRING,
                    required=False,
                    description=(
                        "Natural language description of the task "
                        "you want the agent to perform. This helps "
                        "find agents that match your use case."
                    ),
                    validate_parameter=False,
                ),
            ],
        ),
    )

    grab_web_text: Endpoint = Field(
        default=Endpoint(
            url="/action/grab_web_text",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description=(
                "Extract text content from a specified web page or domain."
            ),
            requires_auth=True,
            response_content_type="application/json",
            request_content_type="application/json",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the web page to extract text from.",
                    validate_parameter=False,
                ),
                EndpointParameter(
                    name="mode",
                    param_type=ParameterType.STRING,
                    required=True,
                    description=(
                        "Crawler mode: 'scrape' for one page,"
                        " 'crawl' for up to 100 pages."
                    ),
                    allowed_values=["scrape", "crawl"],
                    validate_parameter=True,
                ),
            ],
        ),
    )

    grab_web_screenshot: Endpoint = Field(
        default=Endpoint(
            url="/action/grab_web_screenshot",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description=(
                "Capture a visual screenshot of a specified web page for "
                "documentation or analysis."
            ),
            requires_auth=True,
            response_content_type="application/json",
            request_content_type="application/json",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the web page to capture.",
                    validate_parameter=False,
                ),
                EndpointParameter(
                    name="ttl_for_screenshot",
                    param_type=ParameterType.INTEGER,
                    required=True,
                    description=(
                        "Cache expiration time for the screenshot in seconds."
                    ),
                    allowed_values=[3600, 86400, 604800, 18144000],
                    validate_parameter=True,
                ),
            ],
        ),
    )

    get_youtube_transcript: Endpoint = Field(
        default=Endpoint(
            url="/action/get_youtube_transcript",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description=(
                "Fetches the transcript of a YouTube video using"
                " the video URL."
            ),
            requires_auth=True,
            response_content_type="application/json",
            request_content_type="application/json",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the YouTube video.",
                    validate_parameter=False,
                )
            ],
        ),
    )

    get_youtube_channel: Endpoint = Field(
        default=Endpoint(
            url="/action/get_youtube_channel",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description=(
                "Retrieve detailed information about a YouTube channel,"
                " including its videos and statistics."
            ),
            requires_auth=True,
            response_content_type="application/json",
            request_content_type="application/json",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the YouTube channel.",
                    validate_parameter=False,
                )
            ],
        ),
    )

    get_twitter_users: Endpoint = Field(
        default=Endpoint(
            url="/action/get_twitter_users",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description=(
                "Search and retrieve Twitter user profiles based on"
                " specific keywords for targeted social media analysis."
            ),
            requires_auth=True,
            response_content_type="application/json",
            request_content_type="application/json",
            body_parameters=[
                EndpointParameter(
                    name="keywords",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Keywords to find relevant Twitter users.",
                    validate_parameter=False,
                ),
                EndpointParameter(
                    name="num_users",
                    param_type=ParameterType.INTEGER,
                    required=True,
                    description="Number of user profiles to retrieve.",
                    allowed_values=[1, 5, 10, 25, 50, 100],
                    validate_parameter=True,
                ),
            ],
        ),
    )
