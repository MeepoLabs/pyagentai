from pydantic import BaseModel, Field


class AgentAIEndpoints(BaseModel):
    """Endpoints for agent.ai API."""

    # Web URL endpoints - used by the agent.ai web app
    web_list_agents: str = Field(
        default="/agents/list_public", description="Endpoint to list all agents"
    )

    # Get Data endpoints
    api_web_page_content: str = Field(
        default="/action/grab_web_text",
        description="""Extract text content from a specified web
        page or domain.""",
    )
    api_web_page_screenshot: str = Field(
        default="/action/grab_web_screenshot",
        description="Capture a screenshot of a web page.",
    )
    api_youtube_video_transcript: str = Field(
        default="/action/get_youtube_transcript",
        description="""Fetches the transcript
        of a YouTube video using the video URL.""",
    )
    api_youtube_channel_data: str = Field(
        default="/action/get_youtube_channel",
        description="""Retrieve detailed information about a YouTube channel,
        including its videos and statistics.""",
    )
    api_get_twitter_users: str = Field(
        default="/action/get_twitter_users",
        description="""Search and retrieve Twitter user profiles based on
        specific keywords for targeted social media analysis.""",
    )
    api_get_company_earnings_info: str = Field(
        default="/action/company_financial_info",
        description="""Retrieve company earnings information for a given
        stock symbol over time.""",
    )
    api_get_company_financial_profile: str = Field(
        default="/action/company_financial_profile",
        description="""Retrieve detailed financial and company profile
        information for a given stock symbol, such as market cap and the last
        known stock price for any company.""",
    )
    api_get_domain_info: str = Field(
        default="/action/domain_info",
        description="""Retrieve detailed information about a domain, including
        its registration details, DNS records, and more.""",
    )
    api_google_news_data: str = Field(
        default="/action/get_google_news",
        description="""Fetch news articles based on queries and date ranges to
        stay updated on relevant topics or trends.""",
    )
    api_youtube_search_results: str = Field(
        default="/action/run_youtube_search",
        description="""Perform a YouTube search and retrieve results for
        specified queries.""",
    )
    api_search_results: str = Field(
        default="/action/get_search_results",
        description="""Fetch search results from Google or YouTube for
        specific queries, providing valuable insights and content.""",
    )
    api_get_recent_tweets: str = Field(
        default="/action/get_recent_tweets",
        description="""This action fetches recent tweets from a specified
        Twitter handle.""",
    )
    api_get_linkedin_profile: str = Field(
        default="/action/get_linkedin_profile",
        description="""Retrieve detailed information from a specified LinkedIn
        profile for professional insights.""",
    )
    api_get_linkedin_activity: str = Field(
        default="/action/get_linkedin_activity",
        description="""Retrieve recent LinkedIn posts from specified profiles
        to analyze professional activity and engagement.""",
    )
    api_enrich_company_data: str = Field(
        default="/action/get_company_object",
        description="""Gather enriched company data using Breeze Intelligence
        for deeper analysis and insights.""",
    )
    api_get_bluesky_posts: str = Field(
        default="/action/get_bluesky_posts",
        description="""Fetch recent posts from a specified Bluesky user handle,
        making it easy to monitor activity on the platform.""",
    )
    api_search_bluesky_posts: str = Field(
        default="/action/search_bluesky_posts",
        description="""Search for Bluesky posts matching specific keywords or
        criteria to gather social media insights.""",
    )
    api_get_instagram_profile: str = Field(
        default="/action/get_instagram_profile",
        description="""Fetch detailed profile information for a specified
        Instagram username.""",
    )
    api_get_instagram_followers: str = Field(
        default="/action/get_instagram_followers",
        description="""Retrieve a list of top followers from a specified
        Instagram account for social media analysis.""",
    )

    # Use AI endpoints
    api_convert_text_to_speech: str = Field(
        default="/action/output_audio",
        description="Convert text to a generated audio voice file.",
    )
    api_use_llm: str = Field(
        default="/action/invoke_llm",
        description="""Invoke a language model (LLM) to generate text based on
        input instructions, enabling creative and dynamic text outputs.""",
    )
    api_generate_image: str = Field(
        default="/action/generate_image",
        description="""Create visually engaging images using AI models, with
        options for style, aspect ratio, and detailed prompts.""",
    )

    # Advanced endpoints
    api_invoke_agent: str = Field(
        default="/action/invoke_agent",
        description="""Trigger another agent to perform additional processing
        or data handling within workflows.""",
    )
    api_rest_call: str = Field(
        default="/action/rest_call",
        description="Make a REST API call to a specified endpoint.",
    )
    api_convert_file: str = Field(
        default="/action/convert_file",
        description="Convert a file to a different format.",
    )
    api_convert_file_options: str = Field(
        default="/action/convert_file_options",
        description="""Gets the full set of options that a file extension can
        be converted to.""",
    )
    api_start_browser_operator: str = Field(
        default="/action/start_browser_operator",
        description="""Starts a browser operator to interact with web pages
        and perform actions.""",
    )
    api_browser_operator_results: str = Field(
        default="/action/results_browser_operator",
        description="Get the browser operator session results.",
    )
    api_store_variable: str = Field(
        default="/action/store_variable_to_database",
        description="Store a variable in the agent’s database.",
    )
    api_retrieve_variable: str = Field(
        default="/action/get_variable_from_database",
        description="Retrieve a variable from the agent’s database.",
    )

    # Create Output endpoints
    api_create_output: str = Field(
        default="/action/save_to_file",
        description="Save text content as a downloadable file.",
    )
