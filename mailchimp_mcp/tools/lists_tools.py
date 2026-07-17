"""Lists group: list_audience, get_list_info"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    ListAudienceResult,
    ListAudienceData,
    GetListInfoResult,
    GetListInfoData,
)
from ._helpers import _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.lists")


def register_lists_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_audience",
        description="Get information about all lists (audiences) in the account",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_audience() -> ListAudienceResult:
        tlog = ToolLogger(logger, "list_audience")

        try:
            client = service.get_service()
            data = client.lists.get_all_lists()
            tlog.success()
            return ListAudienceResult(success=True, statusCode=200, data=ListAudienceData(**data))
        except Exception as exc:
            return _handle_request_exc(ListAudienceResult, tlog, exc)

    @mcp.tool(
        name="get_list_info",
        description="Get detailed information about a specific list (audience) in your Mailchimp account",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_list_info(
        list_id: str = Field(description="The unique ID for the list"),
    ) -> GetListInfoResult:
        tlog = ToolLogger(logger, "get_list_info")

        try:
            client = service.get_service()
            data = client.lists.get_list(list_id)
            tlog.success()
            return GetListInfoResult(success=True, statusCode=200, data=GetListInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetListInfoResult, tlog, exc)
