"""System group: health_check"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import HealthCheckResult, HealthCheckData
from ._helpers import _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.system")


def register_system_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="health_check",
        description="Check Mailchimp API connectivity",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def health_check() -> HealthCheckResult:
        tlog = ToolLogger(logger, "health_check")

        try:
            client = service.get_service()
            data = client.ping.get()
            tlog.success()
            return HealthCheckResult(success=True, statusCode=200, data=HealthCheckData(**data))
        except Exception as exc:
            return _handle_request_exc(HealthCheckResult, tlog, exc)
