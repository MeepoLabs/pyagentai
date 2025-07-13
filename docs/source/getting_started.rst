Getting Started
===============

This guide will help you get started with `pyagentai` quickly.

Installation
------------

You can install `pyagentai` using pip:

.. code-block:: bash

    pip install pyagentai

Or using Poetry:

.. code-block:: bash

    poetry add pyagentai

Basic Usage
-----------

Here's a simple example of using the `pyagentai` client to find available agents on the agent.ai platform:

.. code-block:: python

    from pyagentai import AgentAIClient
    import asyncio

    async def main():
        # Initialize the client, optionally providing an API key.
        # The client can also be configured using environment variables.
        ag = AgentAIClient(api_key="your_agentai_api_key")

        try:
            # Find the first 10 available agents
            agents = await ag.find_agents(limit=10)
            for agent in agents:
                print(f"- {agent.name}")
        finally:
            # Close the client connection
            await ag.close()

    if __name__ == "__main__":
        asyncio.run(main())

Next Steps
----------

Now that you have a basic understanding of how to use the client, you can explore the full API documentation to discover more features.
