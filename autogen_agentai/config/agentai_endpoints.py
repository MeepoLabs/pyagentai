"""Configuration for agent.ai API endpoints."""

from pydantic import BaseModel, Field

from autogen_agentai.types.url_endpoint import (
    Endpoint,
    EndpointParameter,
    ParameterType,
    RequestMethod,
    UrlType,
)


class AgentAIEndpoints(BaseModel):
    """Endpoints for agent.ai API."""

    # Web URL endpoints - used by the agent.ai web app
    list_agents: Endpoint = Field(
        default=Endpoint(
            url="/agents/list_public",
            url_type=UrlType.WEB,
            method=RequestMethod.POST,
            description="Endpoint to list all agents.",
            requires_auth=False,
            body_parameters=[],
            response_content_type="application/json",
            request_content_type="application/json",
        ),
    )

    get_agent_info: Endpoint = Field(
        default=Endpoint(
            url="/agents/get",
            url_type=UrlType.WEB,
            method=RequestMethod.POST,
            description="Get information about a specific agent.",
            body_parameters=[
                EndpointParameter(
                    name="agent_id",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="ID of the agent to retrieve",
                ),
            ],
        ),
    )

    # Get Data endpoints
    web_page_content: Endpoint = Field(
        default=Endpoint(
            url="/action/grab_web_text",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Extract text content from a specified web page "
            + "or domain.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the web page to extract text from",
                ),
                EndpointParameter(
                    name="mode",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="TBA",
                    default="scrape",
                ),
            ],
        ),
    )

    web_page_screenshot: Endpoint = Field(
        default=Endpoint(
            url="/action/grab_web_screenshot",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Capture a screenshot of a web page.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the web page to capture",
                ),
            ],
            response_content_type="application/json",
        ),
    )

    youtube_video_transcript: Endpoint = Field(
        default=Endpoint(
            url="/action/get_youtube_transcript",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Fetches the transcript of a YouTube video using the "
            + "video URL.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL of the YouTube video",
                ),
            ],
        ),
    )

    youtube_channel_data: Endpoint = Field(
        default=Endpoint(
            url="/action/get_youtube_channel",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve detailed information about a YouTube "
            + "channel.",
            body_parameters=[
                EndpointParameter(
                    name="channelId",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="ID of the YouTube channel",
                ),
            ],
        ),
    )

    get_twitter_users: Endpoint = Field(
        default=Endpoint(
            url="/action/get_twitter_users",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Search and retrieve Twitter user profiles.",
            body_parameters=[
                EndpointParameter(
                    name="query",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Search query for Twitter users",
                ),
            ],
        ),
    )

    get_company_earnings_info: Endpoint = Field(
        default=Endpoint(
            url="/action/company_financial_info",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve company earnings information for a given "
            + "stock symbol.",
            body_parameters=[
                EndpointParameter(
                    name="ticker",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Stock ticker symbol",
                ),
            ],
        ),
    )

    get_company_financial_profile: Endpoint = Field(
        default=Endpoint(
            url="/action/company_financial_profile",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve detailed financial and company profile "
            + "information.",
            body_parameters=[
                EndpointParameter(
                    name="ticker",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Stock ticker symbol",
                ),
            ],
        ),
    )

    get_domain_info: Endpoint = Field(
        default=Endpoint(
            url="/action/domain_info",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve detailed information about a domain.",
            body_parameters=[
                EndpointParameter(
                    name="domain",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Domain name to lookup",
                ),
            ],
        ),
    )

    google_news_data: Endpoint = Field(
        default=Endpoint(
            url="/action/get_google_news",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Fetch news articles based on queries and date "
            + "ranges.",
            body_parameters=[
                EndpointParameter(
                    name="query",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Search query for news articles",
                ),
                EndpointParameter(
                    name="days",
                    param_type=ParameterType.INTEGER,
                    required=False,
                    description="Number of days to look back",
                    default=7,
                ),
            ],
        ),
    )

    youtube_search_results: Endpoint = Field(
        default=Endpoint(
            url="/action/run_youtube_search",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Perform a YouTube search and retrieve results.",
            body_parameters=[
                EndpointParameter(
                    name="query",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Search query for YouTube",
                ),
            ],
        ),
    )

    search_results: Endpoint = Field(
        default=Endpoint(
            url="/action/get_search_results",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Fetch search results from Google or YouTube.",
            body_parameters=[
                EndpointParameter(
                    name="query",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Search query",
                ),
                EndpointParameter(
                    name="source",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="Search source (google or youtube)",
                    default="google",
                ),
            ],
        ),
    )

    get_recent_tweets: Endpoint = Field(
        default=Endpoint(
            url="/action/get_recent_tweets",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Fetch recent tweets from a specified Twitter handle.",
            body_parameters=[
                EndpointParameter(
                    name="handle",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Twitter handle to fetch tweets from",
                ),
            ],
        ),
    )

    get_linkedin_profile: Endpoint = Field(
        default=Endpoint(
            url="/action/get_linkedin_profile",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve detailed information from a LinkedIn "
            + "profile.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="LinkedIn profile URL",
                ),
            ],
        ),
    )

    get_linkedin_activity: Endpoint = Field(
        default=Endpoint(
            url="/action/get_linkedin_activity",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve recent LinkedIn posts from specified "
            + "profiles.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="LinkedIn profile URL",
                ),
            ],
        ),
    )

    enrich_company_data: Endpoint = Field(
        default=Endpoint(
            url="/action/get_company_object",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Gather enriched company data using Breeze "
            + "Intelligence.",
            body_parameters=[
                EndpointParameter(
                    name="company_name",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Name of the company to enrich",
                ),
            ],
        ),
    )

    get_bluesky_posts: Endpoint = Field(
        default=Endpoint(
            url="/action/get_bluesky_posts",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Fetch recent posts from a specified Bluesky user "
            + "handle.",
            body_parameters=[
                EndpointParameter(
                    name="handle",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Bluesky handle to fetch posts from",
                ),
            ],
        ),
    )

    search_bluesky_posts: Endpoint = Field(
        default=Endpoint(
            url="/action/search_bluesky_posts",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Search for Bluesky posts matching specific keywords.",
            body_parameters=[
                EndpointParameter(
                    name="query",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Search query for Bluesky posts",
                ),
            ],
        ),
    )

    get_instagram_profile: Endpoint = Field(
        default=Endpoint(
            url="/action/get_instagram_profile",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Fetch detailed profile information for Instagram.",
            body_parameters=[
                EndpointParameter(
                    name="username",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Instagram username",
                ),
            ],
        ),
    )

    get_instagram_followers: Endpoint = Field(
        default=Endpoint(
            url="/action/get_instagram_followers",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve a list of top followers from an Instagram "
            + "account.",
            body_parameters=[
                EndpointParameter(
                    name="username",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Instagram username",
                ),
            ],
        ),
    )

    # Use AI endpoints
    convert_text_to_speech: Endpoint = Field(
        default=Endpoint(
            url="/action/output_audio",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Convert text to a generated audio voice file.",
            body_parameters=[
                EndpointParameter(
                    name="text",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Text to convert to speech",
                ),
            ],
            response_content_type="audio/mpeg",
        ),
    )

    use_llm: Endpoint = Field(
        default=Endpoint(
            url="/action/invoke_llm",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Invoke a language model to generate text.",
            body_parameters=[
                EndpointParameter(
                    name="model",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="Model to use",
                    default="gpt-4o",
                ),
                EndpointParameter(
                    name="prompt",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Prompt to send to the LLM",
                ),
            ],
        ),
    )

    generate_image: Endpoint = Field(
        default=Endpoint(
            url="/action/generate_image",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Create images using AI models.",
            body_parameters=[
                EndpointParameter(
                    name="prompt",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Text prompt for image generation",
                ),
            ],
            response_content_type="application/json",
        ),
    )

    # Advanced endpoints
    invoke_agent: Endpoint = Field(
        default=Endpoint(
            url="/action/invoke_agent",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Trigger another agent to perform processing.",
            body_parameters=[
                EndpointParameter(
                    name="agentId",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="ID of the agent to invoke",
                ),
                EndpointParameter(
                    name="inputs",
                    param_type=ParameterType.OBJECT,
                    required=True,
                    description="Parameters to pass to the agent",
                ),
            ],
        ),
    )

    rest_call: Endpoint = Field(
        default=Endpoint(
            url="/action/rest_call",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Make a REST API call to a specified endpoint.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="URL to call",
                ),
                EndpointParameter(
                    name="method",
                    param_type=ParameterType.STRING,
                    required=False,
                    description="HTTP method",
                    default="GET",
                ),
            ],
        ),
    )

    convert_file: Endpoint = Field(
        default=Endpoint(
            url="/action/convert_file",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Convert a file to a different format.",
            body_parameters=[
                EndpointParameter(
                    name="file",
                    param_type=ParameterType.FILE,
                    required=True,
                    description="File to convert",
                ),
                EndpointParameter(
                    name="output_format",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Output format",
                ),
            ],
            request_content_type="multipart/form-data",
        ),
    )

    convert_file_options: Endpoint = Field(
        default=Endpoint(
            url="/action/convert_file_options",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Gets file conversion options for a file extension.",
            body_parameters=[
                EndpointParameter(
                    name="extension",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="File extension",
                ),
            ],
        ),
    )

    start_browser_operator: Endpoint = Field(
        default=Endpoint(
            url="/action/start_browser_operator",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Starts a browser operator to interact with web "
            + "pages.",
            body_parameters=[
                EndpointParameter(
                    name="url",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Starting URL",
                ),
            ],
        ),
    )

    browser_operator_results: Endpoint = Field(
        default=Endpoint(
            url="/action/results_browser_operator",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Get the browser operator session results.",
            body_parameters=[
                EndpointParameter(
                    name="session_id",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Browser session ID",
                ),
            ],
        ),
    )

    store_variable: Endpoint = Field(
        default=Endpoint(
            url="/action/store_variable_to_database",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Store a variable in the agent's database.",
            body_parameters=[
                EndpointParameter(
                    name="key",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Variable key",
                ),
                EndpointParameter(
                    name="value",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Variable value",
                ),
            ],
        ),
    )

    retrieve_variable: Endpoint = Field(
        default=Endpoint(
            url="/action/get_variable_from_database",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Retrieve a variable from the agent's database.",
            body_parameters=[
                EndpointParameter(
                    name="key",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Variable key",
                ),
            ],
        ),
    )

    # Create Output endpoints
    create_output: Endpoint = Field(
        default=Endpoint(
            url="/action/save_to_file",
            url_type=UrlType.API,
            method=RequestMethod.POST,
            description="Save text content as a downloadable file.",
            body_parameters=[
                EndpointParameter(
                    name="content",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Content to save",
                ),
                EndpointParameter(
                    name="filename",
                    param_type=ParameterType.STRING,
                    required=True,
                    description="Filename",
                ),
            ],
        ),
    )
