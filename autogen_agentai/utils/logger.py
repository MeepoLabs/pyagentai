"""Logging utilities for autogen-agentai."""

import logging
import os
import sys
from logging import handlers

import structlog

from autogen_agentai.utils.text_processor import sanitize_text

# Get environment variables with defaults
LOG_LEVEL = os.getenv("AGENTAI_LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("AGENTAI_LOG_FORMAT", "json")
LOG_DIR = os.getenv("AGENTAI_LOG_DIR", "logs")
LOG_FILE_ENABLED = (
    os.getenv("AGENTAI_LOG_FILE_ENABLED", "false").lower() == "true"
)
LOG_CONSOLE_ENABLED = (
    os.getenv("AGENTAI_LOG_CONSOLE_ENABLED", "true").lower() == "true"
)
LOG_ROTATE_WHEN = os.getenv("AGENTAI_LOG_ROTATE_WHEN", "W6")
LOG_ROTATE_BACKUP = int(os.getenv("AGENTAI_LOG_ROTATE_BACKUP", "4"))

# Create a mapping of log level strings to their numeric values
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Global flag to track if logging has been initialized
_logging_initialized = False

# Cache for loggers
_logger_cache: dict[str, structlog.stdlib.BoundLogger] = {}


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger with the given name.

    If logging hasn't been initialized yet, this will initialize it with
    default settings.

    Args:
        name: The name of the logger.

    Returns:
        A structured logger.
    """
    global _logging_initialized

    if not _logging_initialized:
        initialize_logging()

    if name in _logger_cache:
        return _logger_cache[name]

    logger: structlog.stdlib.BoundLogger = structlog.get_logger(name)
    _logger_cache[name] = logger
    return logger


def initialize_logging(
    log_level: str | None = None,
    log_format: str | None = None,
    log_dir: str | None = None,
    log_file_enabled: bool | None = None,
    log_console_enabled: bool | None = None,
    log_file_name: str | None = None,
    log_rotate_when: str | None = None,
    log_rotate_backup: int | None = None,
) -> None:
    """Initialize logging for autogen-agentai.

    This function configures structlog for the package. It can be customized
    with various parameters, or it will use environment variables/defaults.

    Args:
        log_level: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: The log format (json or console).
        log_dir: The directory to store log files.
        log_file_enabled: Whether to log to files.
        log_console_enabled: Whether to log to the console.
        log_file_name: Base name for the log file.
        log_rotate_when: When to rotate logs (see TimedRotatingFileHandler).
        log_rotate_backup: Number of backup logs to keep.

    Returns:
        None
    """
    global _logging_initialized

    # Skip if already initialized
    if _logging_initialized:
        return

    # Use provided values or environment variables/defaults
    level = log_level or LOG_LEVEL
    level_num = LOG_LEVEL_MAP.get(level, logging.INFO)
    format_type = log_format or LOG_FORMAT
    directory = log_dir or LOG_DIR
    file_enabled = (
        log_file_enabled if log_file_enabled is not None else LOG_FILE_ENABLED
    )
    console_enabled = (
        log_console_enabled
        if log_console_enabled is not None
        else LOG_CONSOLE_ENABLED
    )
    rotate_when = log_rotate_when or LOG_ROTATE_WHEN
    rotate_backup = (
        log_rotate_backup
        if log_rotate_backup is not None
        else LOG_ROTATE_BACKUP
    )

    # Create handlers list
    handlers_list = []

    # Set up console logging if enabled
    if console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level_num)
        handlers_list.append(console_handler)

    # Set up file logging if enabled
    if file_enabled:
        # Create log directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Use provided file name or default to 'autogen_agentai'
        file_name = log_file_name or "autogen_agentai"
        file_name = sanitize_text(file_name)

        # Configure file handler with rotation
        log_file_path = f"{directory}/{file_name}.log"
        file_handler = handlers.TimedRotatingFileHandler(
            filename=log_file_path,
            when=rotate_when,
            backupCount=rotate_backup,
            encoding="utf-8",
        )
        file_handler.setLevel(level_num)
        handlers_list.append(file_handler)  # type: ignore

    # Configure basic logging
    logging.basicConfig(
        format="%(message)s",
        level=level_num,
        handlers=handlers_list,
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.processors.UnicodeDecoder(),
            # Choose renderer based on format type
            structlog.processors.JSONRenderer()
            if format_type.lower() == "json"
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Mark as initialized
    _logging_initialized = True

    # Get a logger to log the initialization
    logger = structlog.get_logger("autogen_agentai.logging")
    logger.info(
        "Logging initialized",
        level=level,
        format=format_type,
        file_enabled=file_enabled,
        console_enabled=console_enabled,
    )
