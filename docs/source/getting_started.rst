Getting Started
===============

This guide will help you get started with autogen-agentai quickly.

Installation
-----------

You can install autogen-agentai using pip:

.. code-block:: bash

    pip install autogen-agentai

Or using Poetry:

.. code-block:: bash

    poetry add autogen-agentai

Basic Usage
----------

Here's a simple example of using autogen-agentai to connect to agent.ai:

.. code-block:: python

    from autogen_agentai import AgentAIExtension
    import autogen

    # Initialize the extension with your agent.ai API key
    agent_ai_extension = AgentAIExtension(api_key="your_agentai_api_key")

    # Create an AutoGen agent with agent.ai capabilities
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={"config_key": "config_value"},
        extensions=[agent_ai_extension]
    )

    # Now your agent has access to agent.ai capabilities

Next Steps
----------

- Learn about :doc:`core_concepts`
