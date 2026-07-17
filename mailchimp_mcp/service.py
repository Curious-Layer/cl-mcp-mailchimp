"""Upstream API client for MewCP Mailchimp MCP Server."""

import logging

import mailchimp_marketing as MailchimpMarketing
from fastmcp_credentials import get_credentials

logger = logging.getLogger("mailchimp-mcp-server")


def get_service() -> MailchimpMarketing.Client:
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    server_prefix = cred.extra.get("server_prefix")
    if not server_prefix:
        raise ValueError("No server_prefix found in credential extras")
    client = MailchimpMarketing.Client()
    client.set_config({"access_token": cred.access_token, "server": server_prefix})
    return client
