"""Configuration for MewCP Mailchimp MCP Server."""

import logging
import os

from pythonjsonlogger import jsonlogger

SERVER_VERSION = "v1.0.0"

# List breaking changes introduced in this version. Empty for non-breaking releases.
# Each entry: {"tool": str, "change": str, "migration": str}
# The gateway reads this on new server registration to auto-notify affected workflow owners.
BREAKING_CHANGES: list[dict] = []

# Timeouts are not configured here — mailchimp-marketing (the official Mailchimp
# Python SDK) manages its own HTTP transport, same as google-api-python-client
# does for google_calendar_mcp. Timeout enforcement is handled at the gateway level.


def configure_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    handler.setFormatter(
        jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
    )
    logging.basicConfig(level=level, handlers=[handler], force=True)
