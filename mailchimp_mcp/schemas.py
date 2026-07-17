"""Pydantic output schemas for MewCP Mailchimp MCP Server."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Base envelope — shared across all tools
# ---------------------------------------------------------------------------

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


# ---------------------------------------------------------------------------
# Mailchimp Marketing API response models
# extra="allow" lets unmapped API fields pass through without errors — every
# tool in this server returns a raw passthrough of the Mailchimp API response,
# so only ID / pagination / link fields that feed another tool in this server
# are explicitly declared here.
# ---------------------------------------------------------------------------


# ─── 1-6. Automations group ────────────────────────────────────────────────

class AutomationRecipients(BaseModel):
    model_config = ConfigDict(extra="allow")

    list_id: str | None = None
    store_id: str | None = None


class AutomationData(BaseModel):
    """A classic automation workflow — item shape for list_automations,
    also the full shape returned by get_automation_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == workflow_id, consumed by get_automation_info, list_automated_emails, etc.
    create_time: str | None = None
    start_time: str | None = None
    status: str | None = None
    emails_sent: int | None = None
    recipients: AutomationRecipients | None = None


class ListAutomationsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    automations: list[AutomationData] = []
    total_items: int | None = None


class ListAutomationsResult(ToolResult):
    data: ListAutomationsData | None = None


class GetAutomationInfoData(AutomationData):
    """Single automation workflow — same shape as an item in ListAutomationsData."""


class GetAutomationInfoResult(ToolResult):
    data: GetAutomationInfoData | None = None


class AutomationEmailSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    subject_line: str | None = None
    title: str | None = None
    from_name: str | None = None
    reply_to: str | None = None


class AutomationEmailData(BaseModel):
    """A single email step within an automation workflow — item shape for
    list_automated_emails, also the full shape returned by get_workflow_email_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == workflow_email_id, consumed by get_workflow_email_info, list_automated_email_subscribers, etc.
    workflow_id: str | None = None  # parent automation's id
    position: int | None = None
    status: str | None = None
    emails_sent: int | None = None
    send_time: str | None = None
    content_type: str | None = None
    settings: AutomationEmailSettings | None = None


class ListAutomatedEmailsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    emails: list[AutomationEmailData] = []
    total_items: int | None = None


class ListAutomatedEmailsResult(ToolResult):
    data: ListAutomatedEmailsData | None = None


class GetWorkflowEmailInfoData(AutomationEmailData):
    """Single automation email — same shape as an item in ListAutomatedEmailsData."""


class GetWorkflowEmailInfoResult(ToolResult):
    data: GetWorkflowEmailInfoData | None = None


class AutomationSubscriberData(BaseModel):
    """A subscriber queued to receive an automation email — item shape for
    list_automated_email_subscribers, also the full shape returned by
    get_automated_email_subscriber."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == subscriber_hash: MD5 hash of the lowercase email address
    workflow_id: str | None = None
    email_id: str | None = None  # == workflow_email_id of the parent automation email
    list_id: str | None = None
    email_address: str | None = None
    next_send: str | None = None


class ListAutomatedEmailSubscribersData(BaseModel):
    model_config = ConfigDict(extra="allow")

    queue: list[AutomationSubscriberData] = []
    total_items: int | None = None


class ListAutomatedEmailSubscribersResult(ToolResult):
    data: ListAutomatedEmailSubscribersData | None = None


class GetAutomatedEmailSubscriberData(AutomationSubscriberData):
    """Single queued subscriber — same shape as an item in
    ListAutomatedEmailSubscribersData."""


class GetAutomatedEmailSubscriberResult(ToolResult):
    data: GetAutomatedEmailSubscriberData | None = None


# ─── 7-8. Lists (audiences) group ──────────────────────────────────────────

class ListStats(BaseModel):
    model_config = ConfigDict(extra="allow")

    member_count: int | None = None
    unsubscribe_count: int | None = None
    open_rate: float | None = None
    click_rate: float | None = None


class AudienceListData(BaseModel):
    """A single list (audience) — item shape for list_audience, also the full
    shape returned by get_list_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == list_id, consumed by get_list_info and referenced by campaigns/orders
    web_id: int | None = None
    name: str | None = None
    date_created: str | None = None
    stats: ListStats | None = None


class ListAudienceData(BaseModel):
    model_config = ConfigDict(extra="allow")

    lists: list[AudienceListData] = []
    total_items: int | None = None


class ListAudienceResult(ToolResult):
    data: ListAudienceData | None = None


class GetListInfoData(AudienceListData):
    """Single list (audience) — same shape as an item in ListAudienceData."""


class GetListInfoResult(ToolResult):
    data: GetListInfoData | None = None


# ─── 9-12. Campaigns group ─────────────────────────────────────────────────

class CampaignRecipients(BaseModel):
    model_config = ConfigDict(extra="allow")

    list_id: str | None = None
    segment_text: str | None = None
    recipient_count: int | None = None


class CampaignSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    subject_line: str | None = None
    title: str | None = None
    from_name: str | None = None
    reply_to: str | None = None


class CampaignData(BaseModel):
    """A single campaign — item shape for list_campaigns, also the full shape
    returned by get_campaign_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == campaign_id, consumed by get_campaign_info, get_campaign_report, and store orders
    web_id: int | None = None
    type: str | None = None
    create_time: str | None = None
    status: str | None = None
    emails_sent: int | None = None
    send_time: str | None = None
    recipients: CampaignRecipients | None = None
    settings: CampaignSettings | None = None


class ListCampaignsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    campaigns: list[CampaignData] = []
    total_items: int | None = None


class ListCampaignsResult(ToolResult):
    data: ListCampaignsData | None = None


class GetCampaignInfoData(CampaignData):
    """Single campaign — same shape as an item in ListCampaignsData."""


class GetCampaignInfoResult(ToolResult):
    data: GetCampaignInfoData | None = None


class CampaignReportOpens(BaseModel):
    model_config = ConfigDict(extra="allow")

    opens_total: int | None = None
    unique_opens: int | None = None
    open_rate: float | None = None


class CampaignReportClicks(BaseModel):
    model_config = ConfigDict(extra="allow")

    clicks_total: int | None = None
    unique_clicks: int | None = None
    click_rate: float | None = None


class CampaignReportData(BaseModel):
    """A single campaign report — item shape for list_campaign_reports, also
    the full shape returned by get_campaign_report."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == campaign_id, same value used by get_campaign_report / get_campaign_info
    campaign_title: str | None = None
    type: str | None = None
    list_id: str | None = None
    list_name: str | None = None
    emails_sent: int | None = None
    send_time: str | None = None
    opens: CampaignReportOpens | None = None
    clicks: CampaignReportClicks | None = None


class ListCampaignReportsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    reports: list[CampaignReportData] = []
    total_items: int | None = None


class ListCampaignReportsResult(ToolResult):
    data: ListCampaignReportsData | None = None


class GetCampaignReportData(CampaignReportData):
    """Single campaign report — same shape as an item in ListCampaignReportsData."""


class GetCampaignReportResult(ToolResult):
    data: GetCampaignReportData | None = None


# ─── 13-15. Landing pages group ────────────────────────────────────────────

class LandingPageData(BaseModel):
    """A single landing page — item shape for list_landing_pages, also the
    full shape returned by get_landing_page_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == page_id, consumed by get_landing_page_info, get_landing_page_content
    name: str | None = None
    title: str | None = None
    status: str | None = None
    url: str | None = None
    store_id: str | None = None
    list_id: str | None = None
    template_id: int | None = None  # == template_id from the templates group
    created_at: str | None = None
    published_at: str | None = None
    updated_at: str | None = None


class ListLandingPagesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    landing_pages: list[LandingPageData] = []
    total_items: int | None = None


class ListLandingPagesResult(ToolResult):
    data: ListLandingPagesData | None = None


class GetLandingPageInfoData(LandingPageData):
    """Single landing page — same shape as an item in ListLandingPagesData."""


class GetLandingPageInfoResult(ToolResult):
    data: GetLandingPageInfoData | None = None


class GetLandingPageContentData(BaseModel):
    model_config = ConfigDict(extra="allow")

    html: str | None = None


class GetLandingPageContentResult(ToolResult):
    data: GetLandingPageContentData | None = None


# ─── 16-21. Templates group ────────────────────────────────────────────────

class TemplateFolderData(BaseModel):
    """A single template folder — item shape for list_template_folders, also
    the full shape returned by add_template_folder."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == folder_id, consumed by add_template, update_template
    name: str | None = None
    count: int | None = None


class ListTemplateFoldersData(BaseModel):
    model_config = ConfigDict(extra="allow")

    folders: list[TemplateFolderData] = []
    total_items: int | None = None


class ListTemplateFoldersResult(ToolResult):
    data: ListTemplateFoldersData | None = None


class AddTemplateFolderData(TemplateFolderData):
    """Newly created template folder — same shape as an item in ListTemplateFoldersData."""


class AddTemplateFolderResult(ToolResult):
    data: AddTemplateFolderData | None = None


class TemplateData(BaseModel):
    """A single template — item shape for list_templates, also the base shape
    returned by get_template_info, add_template, update_template."""
    model_config = ConfigDict(extra="allow")

    id: int | None = None  # == template_id, consumed by get_template_info, update_template
    type: str | None = None
    name: str | None = None
    date_created: str | None = None
    date_edited: str | None = None
    active: bool | None = None
    folder_id: str | None = None  # == folder_id from list_template_folders / add_template_folder
    thumbnail: str | None = None
    share_url: str | None = None


class ListTemplatesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    templates: list[TemplateData] = []
    total_items: int | None = None


class ListTemplatesResult(ToolResult):
    data: ListTemplatesData | None = None


class GetTemplateInfoData(TemplateData):
    """Single template — same shape as an item in ListTemplatesData, plus the
    rendered HTML which only the single-template fetch returns."""

    html: str | None = None


class GetTemplateInfoResult(ToolResult):
    data: GetTemplateInfoData | None = None


class AddTemplateData(TemplateData):
    """Newly created template — same shape as an item in ListTemplatesData."""


class AddTemplateResult(ToolResult):
    data: AddTemplateData | None = None


class UpdateTemplateData(TemplateData):
    """Updated template — same shape as an item in ListTemplatesData, plus
    before/after state per the MewCP audit rule requiring UPDATE tools to
    return both."""

    before: GetTemplateInfoData | None = None
    after: GetTemplateInfoData | None = None


class UpdateTemplateResult(ToolResult):
    data: UpdateTemplateData | None = None


# ─── 22-27. Ecommerce group ────────────────────────────────────────────────

class StoreData(BaseModel):
    """A single e-commerce store — item shape for list_stores, also the full
    shape returned by get_store_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == store_id, consumed by get_store_info, list_products, list_store_orders
    list_id: str | None = None
    name: str | None = None
    platform: str | None = None
    domain: str | None = None
    currency_code: str | None = None


class ListStoresData(BaseModel):
    model_config = ConfigDict(extra="allow")

    stores: list[StoreData] = []
    total_items: int | None = None


class ListStoresResult(ToolResult):
    data: ListStoresData | None = None


class GetStoreInfoData(StoreData):
    """Single store — same shape as an item in ListStoresData."""


class GetStoreInfoResult(ToolResult):
    data: GetStoreInfoData | None = None


class ProductData(BaseModel):
    """A single product — item shape for list_products, also the full shape
    returned by get_product_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == product_id, consumed by get_product_info
    title: str | None = None
    handle: str | None = None
    url: str | None = None
    type: str | None = None
    vendor: str | None = None
    image_url: str | None = None


class ListProductsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    products: list[ProductData] = []
    total_items: int | None = None


class ListProductsResult(ToolResult):
    data: ListProductsData | None = None


class GetProductInfoData(ProductData):
    """Single product — same shape as an item in ListProductsData."""


class GetProductInfoResult(ToolResult):
    data: GetProductInfoData | None = None


class OrderCustomer(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    email_address: str | None = None


class OrderData(BaseModel):
    """A single order — item shape for list_store_orders, also the full shape
    returned by get_order_info."""
    model_config = ConfigDict(extra="allow")

    id: str | None = None  # == order_id, consumed by get_order_info
    customer: OrderCustomer | None = None
    campaign_id: str | None = None  # == campaign_id from the campaigns group
    financial_status: str | None = None
    fulfillment_status: str | None = None
    currency_code: str | None = None
    order_total: float | None = None
    processed_at_foreign: str | None = None


class ListStoreOrdersData(BaseModel):
    model_config = ConfigDict(extra="allow")

    orders: list[OrderData] = []
    total_items: int | None = None


class ListStoreOrdersResult(ToolResult):
    data: ListStoreOrdersData | None = None


class GetOrderInfoData(OrderData):
    """Single order — same shape as an item in ListStoreOrdersData."""


class GetOrderInfoResult(ToolResult):
    data: GetOrderInfoData | None = None


# ─── 28. System (health_check) ─────────────────────────────────────────────

class HealthCheckData(BaseModel):
    """Response from client.ping.get() — Mailchimp returns a fixed,
    well-known shape: {"health_status": "Everything's Chimpy!"}."""
    model_config = ConfigDict(extra="allow")

    health_status: str | None = None


class HealthCheckResult(ToolResult):
    data: HealthCheckData | None = None
