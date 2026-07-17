"""Templates group: list_template_folders, add_template_folder, list_templates, get_template_info, add_template, update_template"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from typing import Optional

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    ListTemplateFoldersResult,
    ListTemplateFoldersData,
    AddTemplateFolderResult,
    AddTemplateFolderData,
    ListTemplatesResult,
    ListTemplatesData,
    GetTemplateInfoResult,
    GetTemplateInfoData,
    AddTemplateResult,
    AddTemplateData,
    UpdateTemplateResult,
    UpdateTemplateData,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.templates")


def register_templates_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_template_folders",
        description="Get all folders used to organize templates",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_template_folders(
        count: int = Field(default=10, description="Number of folders to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
    ) -> ListTemplateFoldersResult:
        tlog = ToolLogger(logger, "list_template_folders")

        try:
            client = service.get_service()
            data = client.templateFolders.list(count=count, offset=offset)
            tlog.success()
            return ListTemplateFoldersResult(success=True, statusCode=200, data=ListTemplateFoldersData(**data))
        except Exception as exc:
            return _handle_request_exc(ListTemplateFoldersResult, tlog, exc)

    @mcp.tool(
        name="add_template_folder",
        description="Create a new template folder",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def add_template_folder(
        name: str = Field(description="The name of the folder"),
    ) -> AddTemplateFolderResult:
        tlog = ToolLogger(logger, "add_template_folder")

        try:
            client = service.get_service()
            data = client.templateFolders.create({"name": name})
            tlog.success()
            return AddTemplateFolderResult(success=True, statusCode=200, data=AddTemplateFolderData(**data))
        except Exception as exc:
            return _handle_request_exc(AddTemplateFolderResult, tlog, exc)

    @mcp.tool(
        name="list_templates",
        description="Get all templates in your account",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_templates(
        count: int = Field(default=10, description="Number of templates to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
        type: Optional[str] = Field(default=None, description="Filter by type: 'user', 'base', or 'gallery'"),
        content_type: Optional[str] = Field(default=None, description="Filter by content type: 'html', 'template', or 'multichannel'"),
    ) -> ListTemplatesResult:
        tlog = ToolLogger(logger, "list_templates")

        if content_type is not None and content_type not in ("html", "template", "multichannel"):
            return _err(
                ListTemplatesResult, tlog, "VALIDATION_ERROR",
                "Invalid content_type. Must be: html, template, or multichannel", 400,
            )

        query_params = {
            "count": count,
            "offset": offset,
        }
        if type:
            query_params["type"] = type
        if content_type:
            query_params["content_type"] = content_type

        try:
            client = service.get_service()
            data = client.templates.list(**query_params)
            tlog.success()
            return ListTemplatesResult(success=True, statusCode=200, data=ListTemplatesData(**data))
        except Exception as exc:
            return _handle_request_exc(ListTemplatesResult, tlog, exc)

    @mcp.tool(
        name="get_template_info",
        description="Get detailed information about a specific template by ID",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_template_info(
        template_id: str = Field(description="The unique ID for the template"),
    ) -> GetTemplateInfoResult:
        tlog = ToolLogger(logger, "get_template_info")

        try:
            client = service.get_service()
            data = client.templates.get_template(template_id)
            tlog.success()
            return GetTemplateInfoResult(success=True, statusCode=200, data=GetTemplateInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetTemplateInfoResult, tlog, exc)

    @mcp.tool(
        name="add_template",
        description="Create a new Classic template for the account. It supports Mailchimp Template Language",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def add_template(
        name: str = Field(description="The name of the template"),
        html: str = Field(description="The raw HTML for the template. Supports Mailchimp Template Language"),
        folder_id: Optional[str] = Field(default=None, description="The ID of the folder to place the template in"),
    ) -> AddTemplateResult:
        tlog = ToolLogger(logger, "add_template")

        body = {"name": name, "html": html}
        if folder_id:
            body["folder_id"] = folder_id

        try:
            client = service.get_service()
            data = client.templates.create(body)
            tlog.success()
            return AddTemplateResult(success=True, statusCode=200, data=AddTemplateData(**data))
        except Exception as exc:
            return _handle_request_exc(AddTemplateResult, tlog, exc)

    @mcp.tool(
        name="update_template",
        description=(
            "Updates the name, HTML, or folder of an existing Classic template. "
            "This overwrites the current name and HTML with the values you provide (folder_id "
            "is only changed if given) — the original state is not stored by the API after "
            "the call. The response includes both the before and after state so you have a "
            "full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_template(
        template_id: str = Field(description="The unique ID for the template"),
        name: str = Field(description="The name of the template"),
        html: str = Field(description="The raw HTML for the template. Supports Mailchimp Template Language"),
        folder_id: Optional[str] = Field(default=None, description="The ID of the folder to move the template to"),
    ) -> UpdateTemplateResult:
        tlog = ToolLogger(logger, "update_template")

        body = {"name": name, "html": html}
        if folder_id:
            body["folder_id"] = folder_id

        try:
            client = service.get_service()
            before = client.templates.get_template(template_id)
            after = client.templates.update_template(template_id, body)
            tlog.success()
            return UpdateTemplateResult(
                success=True, statusCode=200,
                data=UpdateTemplateData(
                    before=GetTemplateInfoData(**before),
                    after=GetTemplateInfoData(**after),
                ),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateTemplateResult, tlog, exc)
