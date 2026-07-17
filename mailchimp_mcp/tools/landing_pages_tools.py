"""Landing pages group: list_landing_pages, get_landing_page_info, get_landing_page_content"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from typing import Optional

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    ListLandingPagesResult,
    ListLandingPagesData,
    GetLandingPageInfoResult,
    GetLandingPageInfoData,
    GetLandingPageContentResult,
    GetLandingPageContentData,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.landing_pages")


def register_landing_pages_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_landing_pages",
        description="Get all landing pages in your account",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_landing_pages(
        count: int = Field(default=10, description="Number of landing pages to return (max: 1000)"),
        sort_field: Optional[str] = Field(default=None, description="Sort by: 'created_at' or 'updated_at'"),
        sort_dir: Optional[str] = Field(default=None, description="Sort direction: 'ASC' or 'DESC'"),
    ) -> ListLandingPagesResult:
        tlog = ToolLogger(logger, "list_landing_pages")

        if sort_field is not None and sort_field not in ("created_at", "updated_at"):
            return _err(
                ListLandingPagesResult, tlog, "VALIDATION_ERROR",
                "Invalid sort_field. Must be: created_at or updated_at", 400,
            )

        if sort_dir is not None and sort_dir.upper() not in ("ASC", "DESC"):
            return _err(
                ListLandingPagesResult, tlog, "VALIDATION_ERROR",
                "Invalid sort_dir. Must be: ASC or DESC", 400,
            )

        query_params = {"count": count}
        if sort_field is not None:
            query_params["sort_field"] = sort_field
        if sort_dir is not None:
            query_params["sort_dir"] = sort_dir.upper()

        try:
            client = service.get_service()
            data = client.landingPages.get_all(**query_params)
            tlog.success()
            return ListLandingPagesResult(success=True, statusCode=200, data=ListLandingPagesData(**data))
        except Exception as exc:
            return _handle_request_exc(ListLandingPagesResult, tlog, exc)

    @mcp.tool(
        name="get_landing_page_info",
        description="Get detailed information about a specific landing page by ID",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_landing_page_info(
        page_id: str = Field(description="The unique ID for the landing page"),
    ) -> GetLandingPageInfoResult:
        tlog = ToolLogger(logger, "get_landing_page_info")

        try:
            client = service.get_service()
            data = client.landingPages.get_page(page_id)
            tlog.success()
            return GetLandingPageInfoResult(success=True, statusCode=200, data=GetLandingPageInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetLandingPageInfoResult, tlog, exc)

    @mcp.tool(
        name="get_landing_page_content",
        description="Get the HTML content for a specific landing page",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_landing_page_content(
        page_id: str = Field(description="The unique ID for the landing page"),
    ) -> GetLandingPageContentResult:
        tlog = ToolLogger(logger, "get_landing_page_content")

        try:
            client = service.get_service()
            data = client.landingPages.get_page_content(page_id)
            tlog.success()
            return GetLandingPageContentResult(success=True, statusCode=200, data=GetLandingPageContentData(**data))
        except Exception as exc:
            return _handle_request_exc(GetLandingPageContentResult, tlog, exc)
