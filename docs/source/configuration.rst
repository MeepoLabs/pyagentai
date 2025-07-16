Configuration
=============

This section provides detailed guidance on configuring the `pyagentai` client, including setting up logging and managing API credentials.

Configuring the Client
----------------------

The ``AgentAIClient`` can be configured in several ways to suit your application's needs.

Using `AgentAIConfig`
~~~~~~~~~~~~~~~~~~~~~

The ``AgentAIConfig`` class allows you to define all client settings in one place. You can create an instance of this class and pass it to the ``AgentAIClient`` constructor.

.. code-block:: python

    from pyagentai import AgentAIClient, AgentAIConfig

    # Create a custom configuration
    config = AgentAIConfig(
        api_key="your_custom_api_key",
        timeout=120.0
    )

    # Initialize the client with the custom configuration
    client = AgentAIClient(config=config)

Direct Initialization
~~~~~~~~~~~~~~~~~~~~~

For quick setup, you can pass the API key directly to the ``AgentAIClient`` constructor. Other settings will use default values.

.. code-block:: python

    from pyagentai import AgentAIClient

    # Initialize the client with an API key
    client = AgentAIClient(api_key="your_agentai_api_key")

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The client can also be configured using environment variables. This is particularly useful in production environments.

-   ``AGENTAI_API_KEY``: Your agent.ai API key.
-   ``AGENTAI_API_URL``: The base URL for the agent.ai API.
-   ``AGENTAI_WEB_URL``: The URL for the agent.ai web application.

.. code-block:: python

    import os
    from pyagentai import AgentAIClient

    # Set environment variables before initializing the client
    os.environ["AGENTAI_API_KEY"] = "your_api_key_from_env"

    # The client will automatically pick up the settings
    client = AgentAIClient()

Loading from YAML
~~~~~~~~~~~~~~~~~

For more complex configurations, you can load settings from a YAML file.

.. code-block:: yaml
    :caption: config.yaml

    api_key: "your_api_key_from_yaml"
    timeout: 90.0

.. code-block:: python

    from pyagentai import AgentAIConfig, AgentAIClient

    # Load configuration from a YAML file
    config = AgentAIConfig.from_yaml("config.yaml")
    client = AgentAIClient(config=config)


Configuring Logging
-------------------

`pyagentai` uses the `structlog` library for logging, which is highly configurable.

Using the `configure_logging` function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to set up logging is with the ``configure_logging`` function from the ``pyagentai`` package.

.. code-block:: python

    from pyagentai import configure_logging

    # Configure logging with a specific log level and format
    configure_logging(log_level="DEBUG", log_format="json")

Logging with Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also configure logging using environment variables, which is ideal for containerized or production environments.

-   ``AGENTAI_LOG_LEVEL``: Log level (e.g., `DEBUG`, `INFO`, `WARNING`).
-   ``AGENTAI_LOG_FORMAT``: Log format (`console` or `json`).
-   ``AGENTAI_LOG_FILE_ENABLED``: Set to `true` to enable file logging.
-   ``AGENTAI_LOG_DIR``: Directory to store log files.
-   ``AGENTAI_LOG_FILE_NAME``: Name of the log file.

Example:

.. code-block:: bash

    export AGENTAI_LOG_LEVEL="DEBUG"
    export AGENTAI_LOG_FILE_ENABLED="true"
    export AGENTAI_LOG_DIR="/var/log/pyagentai"

The library will automatically apply these settings when it is imported.
