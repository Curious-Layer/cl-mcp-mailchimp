"""Automations group: list_automations, get_automation_info, list_automated_emails,
get_workflow_email_info, list_automated_email_subscribers, get_automated_email_subscriber."""

from __future__ import annotations

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from ..logging_utils import ToolLogger
from ..schemas import (
    GetAutomatedEmailSubscriberData,
    GetAutomatedEmailSubscriberResult,
    GetAutomationInfoData,
    GetAutomationInfoResult,
    GetWorkflowEmailInfoData,
    GetWorkflowEmailInfoResult,
    ListAutomatedEmailsData,
    ListAutomatedEmailsResult,
    ListAutomatedEmailSubscribersData,
    ListAutomatedEmailSubscribersResult,
    ListAutomationsData,
    ListAutomationsResult,
)
from ..service import get_service
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.automations")


def register_automations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_automations",
        description="Get a summary of an account's classic automations with optional filtering and pagination",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_automations(
        count: int = Field(default=10, description="Number of records to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
        fields: str | None = Field(default=None, description="Comma-separated list of fields to return"),
        exclude_fields: str | None = Field(default=None, description="Comma-separated list of fields to exclude"),
        before_create_time: str | None = Field(default=None, description="Restrict to automations created before this time (ISO 8601: 2015-10-21T15:41:36+00:00)"),
        since_create_time: str | None = Field(default=None, description="Restrict to automations created after this time (ISO 8601: 2015-10-21T15:41:36+00:00)"),
        before_start_time: str | None = Field(default=None, description="Restrict to automations started before this time (ISO 8601: 2015-10-21T15:41:36+00:00)"),
        since_start_time: str | None = Field(default=None, description="Restrict to automations started after this time (ISO 8601: 2015-10-21T15:41:36+00:00)"),
        status: str | None = Field(default=None, description="Filter by status: 'save', 'paused', or 'sending'"),
    ) -> ListAutomationsResult:
        tlog = ToolLogger(logger, "list_automations")

        if status not in (None, "save", "paused", "sending"):
            return _err(
                ListAutomationsResult, tlog, "VALIDATION_ERROR",
                "Invalid status. Must be one of: save, paused, sending", 400,
            )

        query_params: dict = {"count": count, "offset": offset}
        if fields:
            query_params["fields"] = fields
        if exclude_fields:
            query_params["exclude_fields"] = exclude_fields
        if before_create_time:
            query_params["before_create_time"] = before_create_time
        if since_create_time:
            query_params["since_create_time"] = since_create_time
        if before_start_time:
            query_params["before_start_time"] = before_start_time
        if since_start_time:
            query_params["since_start_time"] = since_start_time
        if status:
            query_params["status"] = status

        try:
            client = get_service()
            raw = client.automations.list(**query_params)
            tlog.success()
            return ListAutomationsResult(success=True, statusCode=200, data=ListAutomationsData(**raw))
        except Exception as exc:
            return _handle_request_exc(ListAutomationsResult, tlog, exc)

    @mcp.tool(
        name="get_automation_info",
        description="Get detailed information about a specific automation workflow by ID",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_automation_info(
        workflow_id: str = Field(description="The unique ID of the Automation workflow"),
        fields: str | None = Field(default=None, description="Comma-separated list of fields to return"),
        exclude_fields: str | None = Field(default=None, description="Comma-separated list of fields to exclude"),
    ) -> GetAutomationInfoResult:
        tlog = ToolLogger(logger, "get_automation_info")

        query_params: dict = {}
        if fields:
            query_params["fields"] = fields
        if exclude_fields:
            query_params["exclude_fields"] = exclude_fields

        try:
            client = get_service()
            raw = client.automations.get(workflow_id, **query_params)
            tlog.success()
            return GetAutomationInfoResult(success=True, statusCode=200, data=GetAutomationInfoData(**raw))
        except Exception as exc:
            return _handle_request_exc(GetAutomationInfoResult, tlog, exc)

    @mcp.tool(
        name="list_automated_emails",
        description="Get a summary of the emails in a classic automation workflow",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_automated_emails(
        workflow_id: str = Field(description="The unique ID of the Automation workflow"),
    ) -> ListAutomatedEmailsResult:
        tlog = ToolLogger(logger, "list_automated_emails")
        try:
            client = get_service()
            raw = client.automations.list_all_workflow_emails(workflow_id)
            tlog.success()
            return ListAutomatedEmailsResult(success=True, statusCode=200, data=ListAutomatedEmailsData(**raw))
        except Exception as exc:
            return _handle_request_exc(ListAutomatedEmailsResult, tlog, exc)

    @mcp.tool(
        name="get_workflow_email_info",
        description="Get detailed information about a specific email in an automation workflow",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_workflow_email_info(
        workflow_id: str = Field(description="The unique ID of the Automation workflow"),
        workflow_email_id: str = Field(description="The unique ID of the Automation workflow email"),
    ) -> GetWorkflowEmailInfoResult:
        """Returns:
        - Email position in the workflow sequence
        - Delay settings (when email sends relative to trigger)
        - Subject line, preview text, and content details
        - From name, reply-to, and sender settings
        - Recipients list and segment configuration
        - Tracking configuration (opens, clicks, Google Analytics)
        - Social media integration (auto-tweet, Facebook)
        - Performance metrics (open rate, click rate, sends)
        - Template and content type information
        - Current status (save, paused, sending)
        """
        tlog = ToolLogger(logger, "get_workflow_email_info")
        try:
            client = get_service()
            raw = client.automations.get_workflow_email(workflow_id, workflow_email_id)
            tlog.success()
            return GetWorkflowEmailInfoResult(success=True, statusCode=200, data=GetWorkflowEmailInfoData(**raw))
        except Exception as exc:
            return _handle_request_exc(GetWorkflowEmailInfoResult, tlog, exc)

    @mcp.tool(
        name="list_automated_email_subscribers",
        description="Get information about subscribers queued to receive a specific automation email",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_automated_email_subscribers(
        workflow_id: str = Field(description="The unique ID of the Automation workflow"),
        workflow_email_id: str = Field(description="The unique ID of the Automation workflow email"),
    ) -> ListAutomatedEmailSubscribersResult:
        tlog = ToolLogger(logger, "list_automated_email_subscribers")
        try:
            client = get_service()
            raw = client.automations.get_workflow_email_subscriber_queue(workflow_id, workflow_email_id)
            tlog.success()
            return ListAutomatedEmailSubscribersResult(
                success=True, statusCode=200, data=ListAutomatedEmailSubscribersData(**raw),
            )
        except Exception as exc:
            return _handle_request_exc(ListAutomatedEmailSubscribersResult, tlog, exc)

    @mcp.tool(
        name="get_automated_email_subscriber",
        description="Get detailed information about a specific subscriber to an automation email queue",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_automated_email_subscriber(
        workflow_id: str = Field(description="The unique ID of the Automation workflow"),
        workflow_email_id: str = Field(description="The unique ID of the Automation workflow email"),
        subscriber_hash: str = Field(description="The MD5 hash of the lowercase version of the subscriber's email address"),
    ) -> GetAutomatedEmailSubscriberResult:
        tlog = ToolLogger(logger, "get_automated_email_subscriber")
        try:
            client = get_service()
            raw = client.automations.get_workflow_email_subscriber(
                workflow_id, workflow_email_id, subscriber_hash,
            )
            tlog.success()
            return GetAutomatedEmailSubscriberResult(
                success=True, statusCode=200, data=GetAutomatedEmailSubscriberData(**raw),
            )
        except Exception as exc:
            return _handle_request_exc(GetAutomatedEmailSubscriberResult, tlog, exc)
