from urllib.parse import urlparse

from pyagentai.client import AgentAIClient


@AgentAIClient.register
async def grab_web_text(
    self: AgentAIClient,
    url: str,
    mode: str = "scrape",
) -> tuple[str, dict]:
    """Extract text content from a specified web page or domain.

    Args:
        url: URL of the web page to extract text from.
        mode: Crawler mode: 'scrape' for one page, 'crawl' for up to 100 pages.

    Returns:
        Text content of the web page or domain.
    """
    endpoint = self.config.endpoints.grab_web_text
    data = {}
    parameters = {
        "url": url,
        "mode": mode,
    }

    # validate URL
    try:
        parsed_url = urlparse(url)

        # We check for a valid scheme (http/https) and a domain.
        if not (parsed_url.scheme in ["http", "https"] and parsed_url.netloc):
            raise ValueError(
                "URL must have a valid scheme (http/https) and domain name."
            )

    except (ValueError, AttributeError) as e:
        error_message = f"Invalid URL provided: '{url}'"
        await self._logger.error(error_message, url=url)
        raise ValueError(error_message) from e

    for key, value in parameters.items():
        if value is not None and value.strip():
            # URL should not be lowercased as the path can be case-sensitive.
            if key == "url":
                data[key] = value.strip()
            else:
                data[key] = value.strip().lower()

    response = await self._make_request(
        endpoint=endpoint,
        data=data,
    )
    response_data = response.json()

    # The API returns responses in an unformatted string
    # It contains a metadata JSON and content text
    # TODO: format the response data
    response_text: str = response_data.get("response", "")
    metadata: dict = response_data.get("metadata", {})

    return response_text, metadata
