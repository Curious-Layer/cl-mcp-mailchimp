"""Campaigns group: list_campaigns, get_campaign_info, list_campaign_reports, get_campaign_report"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from typing import Optional

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    ListCampaignsResult,
    ListCampaignsData,
    GetCampaignInfoResult,
    GetCampaignInfoData,
    ListCampaignReportsResult,
    ListCampaignReportsData,
    GetCampaignReportResult,
    GetCampaignReportData,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.campaigns")


def register_campaigns_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_campaigns",
        description="Get all campaigns in an account",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_campaigns() -> ListCampaignsResult:
        tlog = ToolLogger(logger, "list_campaigns")

        try:
            client = service.get_service()
            data = client.campaigns.list()
            tlog.success()
            return ListCampaignsResult(success=True, statusCode=200, data=ListCampaignsData(**data))
        except Exception as exc:
            return _handle_request_exc(ListCampaignsResult, tlog, exc)

    @mcp.tool(
        name="get_campaign_info",
        description="Get detailed information about a specific campaign",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_campaign_info(
        campaign_id: str = Field(description="The unique ID for the campaign"),
    ) -> GetCampaignInfoResult:
        tlog = ToolLogger(logger, "get_campaign_info")

        try:
            client = service.get_service()
            data = client.campaigns.get(campaign_id)
            tlog.success()
            return GetCampaignInfoResult(success=True, statusCode=200, data=GetCampaignInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetCampaignInfoResult, tlog, exc)

    @mcp.tool(
        name="list_campaign_reports",
        description="Get all campaign reports with performance metrics",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_campaign_reports(
        count: int = Field(default=10, description="Number of reports to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
        type: Optional[str] = Field(default=None, description="Filter by campaign type: 'regular', 'plaintext', 'absplit', 'rss', or 'variate'"),
    ) -> ListCampaignReportsResult:
        tlog = ToolLogger(logger, "list_campaign_reports")

        if type not in (None, "regular", "plaintext", "absplit", "rss", "variate"):
            return _err(
                ListCampaignReportsResult, tlog, "VALIDATION_ERROR",
                "Invalid type. Must be one of: regular, plaintext, absplit, rss, variate", 400,
            )

        query_params = {
            "count": count,
            "offset": offset,
        }
        if type:
            query_params["type"] = type

        try:
            client = service.get_service()
            data = client.reports.get_all_campaign_reports(**query_params)
            tlog.success()
            return ListCampaignReportsResult(success=True, statusCode=200, data=ListCampaignReportsData(**data))
        except Exception as exc:
            return _handle_request_exc(ListCampaignReportsResult, tlog, exc)

    @mcp.tool(
        name="get_campaign_report",
        description="Get detailed report for a specific sent campaign",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_campaign_report(
        campaign_id: str = Field(description="The unique ID for the campaign"),
    ) -> GetCampaignReportResult:
        tlog = ToolLogger(logger, "get_campaign_report")

        try:
            client = service.get_service()
            data = client.reports.get_campaign_report(campaign_id)
            tlog.success()
            return GetCampaignReportResult(success=True, statusCode=200, data=GetCampaignReportData(**data))
        except Exception as exc:
            return _handle_request_exc(GetCampaignReportResult, tlog, exc)
