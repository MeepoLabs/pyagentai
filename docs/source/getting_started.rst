Getting Started
===============

This guide will help you get started with `pyagentai` quickly. Before you
begin, please follow the :doc:`installation` guide.

Initializing the Client
-----------------------

The ``AgentAIClient`` is the main entry point for interacting with the
agent.ai API. You can initialize it in several ways.

The simplest way is to provide your API key directly:

.. code-block:: python

    from pyagentai import AgentAIClient

    client = AgentAIClient(api_key="your_agentai_api_key")

For more advanced configuration options, see the :doc:`configuration` guide.

Using the Client
----------------

Once the client is initialized, you can use its methods to interact with
the API. All API methods are asynchronous and must be awaited.

Finding Agents
~~~~~~~~~~~~~~

Here's a simple example of using the ``find_agents`` method to discover
available agents:

.. code-block:: python

    import asyncio
    from pyagentai import AgentAIClient

    async def main():
        client = AgentAIClient(api_key="your_agentai_api_key")

        try:
            # Find the first 10 available agents
            agents = await client.find_agents(limit=10)
            for agent in agents:
                print(f"- Agent: {agent.name}, ID: {agent.agent_id}")
        finally:
            # Close the client connection
            await client.close()

    if __name__ == "__main__":
        asyncio.run(main())

Grabbing Web Text
~~~~~~~~~~~~~~~~~

You can also use the client to extract text from a web page:

.. code-block:: python

    import asyncio
    from pyagentai import AgentAIClient

    async def main():
        client = AgentAIClient(api_key="your_agentai_api_key")

        try:
            url_to_scrape = "https://example.com"
            text, metadata = await client.grab_web_text(url=url_to_scrape)
            print(f"Scraped text from {url_to_scrape}:")
            print(text[:200] + "...")  # Print the first 200 characters
        finally:
            await client.close()

    if __name__ == "__main__":
        asyncio.run(main())


Next Steps
----------

Now that you have a basic understanding of how to use the client, you can
explore the full :doc:`api_reference` to discover more features and data
types.
