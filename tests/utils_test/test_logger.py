import importlib
import json
import logging
import os
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
import structlog
from _pytest.logging import LogCaptureFixture

from pyagentai.utils import logger
from pyagentai.utils.text_processor import sanitize_text


@pytest.fixture(autouse=True)
def reset_logging_state(
    monkeypatch: pytest.MonkeyPatch
) -> Generator[None, None, None]:
    """Ensure a clean logging state for each test."""
    # Unset all relevant environment variables
    for var in [
        "AGENTAI_LOG_LEVEL",
        "AGENTAI_LOG_FORMAT",
        "AGENTAI_LOG_DIR",
        "AGENTAI_LOG_FILE_ENABLED",
        "AGENTAI_LOG_CONSOLE_ENABLED",
        "AGENTAI_LOG_ROTATE_BACKUP",
    ]:
        monkeypatch.delenv(var, raising=False)

    # Reset structlog and standard logging
    structlog.reset_defaults()
    root_logger = logging.getLogger("pyagentai")
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Reload the logger module to apply a clean state
    importlib.reload(logger)
    yield None

    # Post-test cleanup
    structlog.reset_defaults()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)


def test_default_logging_is_null() -> None:
    """Test that by default, no handlers are configured."""
    root_logger = logging.getLogger("pyagentai")
    assert isinstance(root_logger.handlers[0], logging.NullHandler)


@pytest.mark.asyncio()
async def test_initialize_logging_console(caplog: LogCaptureFixture) -> None:
    """Test console logging initialization."""
    logger.initialize_logging(log_console_enabled=True, log_level="INFO")
    log = structlog.get_logger("pyagentai")

    with caplog.at_level(logging.INFO):
        await log.info("test message")
        assert "test message" in caplog.text


def test_initialize_logging_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test file logging initialization."""
    mock_makedirs = MagicMock()
    monkeypatch.setattr(os, "makedirs", mock_makedirs)
    mock_file_handler = MagicMock()
    monkeypatch.setattr(
        logging.handlers,
        "TimedRotatingFileHandler",
        lambda **kwargs: mock_file_handler,
    )

    logger.initialize_logging(
        log_file_enabled=True, log_dir="test_logs", log_file_name="test_app"
    )

    mock_makedirs.assert_called_once_with("test_logs", exist_ok=True)
    mock_file_handler.setLevel.assert_called_once_with(logging.INFO)

    root_logger = logging.getLogger("pyagentai")
    assert mock_file_handler in root_logger.handlers


@pytest.mark.asyncio()
async def test_logging_level(caplog: LogCaptureFixture) -> None:
    """Test that the log level is respected."""
    logger.initialize_logging(log_console_enabled=True, log_level="WARNING")
    log = structlog.get_logger("pyagentai")

    await log.info("this should be ignored")
    await log.warning("this should be captured")

    assert "this should be ignored" not in caplog.text
    assert "this should be captured" in caplog.text


@pytest.mark.asyncio()
async def test_json_log_format(caplog: LogCaptureFixture) -> None:
    """Test JSON formatting for logs."""
    logger.initialize_logging(
        log_console_enabled=True, log_level="INFO", log_format="json"
    )
    log = structlog.get_logger("pyagentai")

    with caplog.at_level(logging.INFO):
        await log.info("json test", key="value")
        # The last record's message is the entire JSON string
        log_record = json.loads(caplog.records[-1].message)
        assert log_record["event"] == "json test"
        assert log_record["key"] == "value"


def test_reinitialization_removes_old_handlers(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that re-initializing the logger removes old handlers."""
    # Initial setup with console
    logger.initialize_logging(log_console_enabled=True)
    root_logger = logging.getLogger("pyagentai")
    assert any(
        isinstance(h, logging.StreamHandler) for h in root_logger.handlers
    )

    # Mock for file handler part
    mock_file_handler = MagicMock()
    monkeypatch.setattr(
        logging.handlers,
        "TimedRotatingFileHandler",
        lambda **kwargs: mock_file_handler,
    )
    monkeypatch.setattr(os, "makedirs", MagicMock())

    # Re-initialize with file logging
    logger.initialize_logging(log_file_enabled=True, log_console_enabled=False)
    assert not any(
        isinstance(h, logging.StreamHandler) for h in root_logger.handlers
    )
    assert mock_file_handler in root_logger.handlers


@pytest.mark.asyncio()
async def test_env_var_configuration(
    monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    """Test that logging can be configured from environment variables."""
    monkeypatch.setenv("AGENTAI_LOG_CONSOLE_ENABLED", "true")
    monkeypatch.setenv("AGENTAI_LOG_LEVEL", "DEBUG")

    # Reload the module to trigger auto-configuration
    importlib.reload(logger)
    log = structlog.get_logger("pyagentai")

    with caplog.at_level(logging.DEBUG):
        await log.debug("configured from env")
        assert "configured from env" in caplog.text


@pytest.mark.asyncio()
async def test_invalid_log_level_defaults_to_info(
    caplog: LogCaptureFixture
) -> None:
    """Test that providing an invalid log level string defaults to INFO."""
    logger.initialize_logging(
        log_console_enabled=True, log_level="INVALID_LEVEL"
    )
    root_logger = logging.getLogger("pyagentai")

    assert root_logger.level == logging.INFO
    with caplog.at_level(logging.INFO):
        log = structlog.get_logger("pyagentai")
        await log.info("info message")
        assert "info message" in caplog.text


def test_file_creation_permission_error(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that a PermissionError during log dir creation is handled."""
    monkeypatch.setattr(os, "makedirs", MagicMock(side_effect=PermissionError))
    logger.initialize_logging(log_file_enabled=True)

    root_logger = logging.getLogger("pyagentai")
    assert not any(
        isinstance(h, logging.FileHandler) for h in root_logger.handlers
    )


def test_both_logging_disabled() -> None:
    """Test that a NullHandler is present when all logging is disabled."""
    logger.initialize_logging(
        log_file_enabled=False,
        log_console_enabled=False,
    )
    root_logger = logging.getLogger("pyagentai")
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.NullHandler)


def test_log_file_name_sanitization(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that log file names are properly sanitized before use."""
    mock_handler_constructor = MagicMock()
    monkeypatch.setattr(
        logging.handlers, "TimedRotatingFileHandler", mock_handler_constructor
    )
    monkeypatch.setattr(os, "makedirs", MagicMock())

    invalid_name = 'invalid/name*?"'
    sanitized_name = sanitize_text(invalid_name)
    expected_path = f"logs/{sanitized_name}.log"

    logger.initialize_logging(
        log_file_enabled=True,
        log_file_name=invalid_name,
    )
    mock_handler_constructor.assert_called_once()
    _, kwargs = mock_handler_constructor.call_args
    assert kwargs["filename"] == expected_path


def test_env_var_malformed_backup_count(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that an invalid backup count from env vars is handled."""
    monkeypatch.setenv("AGENTAI_LOG_FILE_ENABLED", "true")
    monkeypatch.setenv("AGENTAI_LOG_ROTATE_BACKUP", "not-a-number")

    # The current implementation will raise a ValueError
    with pytest.raises(ValueError, match="invalid literal for int"):
        importlib.reload(logger)


def test_invalid_backup_count_handling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a negative backup count is handled by the file handler."""
    mock_handler_constructor = MagicMock()
    monkeypatch.setattr(
        logging.handlers, "TimedRotatingFileHandler", mock_handler_constructor
    )
    monkeypatch.setattr(os, "makedirs", MagicMock())

    logger.initialize_logging(log_file_enabled=True, log_rotate_backup=-1)

    mock_handler_constructor.assert_called_once()
    _, kwargs = mock_handler_constructor.call_args
    assert kwargs["backupCount"] == -1
