from fastmcp import FastMCP

from .automations_tools import register_automations_tools
from .campaigns_tools import register_campaigns_tools
from .ecommerce_tools import register_ecommerce_tools
from .landing_pages_tools import register_landing_pages_tools
from .lists_tools import register_lists_tools
from .system_tools import register_system_tools
from .templates_tools import register_templates_tools


def register_tools(mcp: FastMCP) -> None:
    register_automations_tools(mcp)
    register_lists_tools(mcp)
    register_campaigns_tools(mcp)
    register_landing_pages_tools(mcp)
    register_templates_tools(mcp)
    register_ecommerce_tools(mcp)
    register_system_tools(mcp)
