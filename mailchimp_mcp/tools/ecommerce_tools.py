"""Ecommerce group: list_stores, get_store_info, list_products, get_product_info, list_store_orders, get_order_info"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from typing import Optional

from .. import service
from ..logging_utils import ToolLogger
from ..schemas import (
    ListStoresResult,
    ListStoresData,
    GetStoreInfoResult,
    GetStoreInfoData,
    ListProductsResult,
    ListProductsData,
    GetProductInfoResult,
    GetProductInfoData,
    ListStoreOrdersResult,
    ListStoreOrdersData,
    GetOrderInfoResult,
    GetOrderInfoData,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("mailchimp-mcp.tools.ecommerce")


def register_ecommerce_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_stores",
        description="Get information about all e-commerce stores in the account",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_stores(
        count: int = Field(default=10, description="Number of stores to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
    ) -> ListStoresResult:
        tlog = ToolLogger(logger, "list_stores")

        try:
            client = service.get_service()
            data = client.ecommerce.stores(count=count, offset=offset)
            tlog.success()
            return ListStoresResult(success=True, statusCode=200, data=ListStoresData(**data))
        except Exception as exc:
            return _handle_request_exc(ListStoresResult, tlog, exc)

    @mcp.tool(
        name="get_store_info",
        description="Get detailed information about a specific e-commerce store",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_store_info(
        store_id: str = Field(description="The unique ID for the store"),
    ) -> GetStoreInfoResult:
        tlog = ToolLogger(logger, "get_store_info")

        try:
            client = service.get_service()
            data = client.ecommerce.get_store(store_id)
            tlog.success()
            return GetStoreInfoResult(success=True, statusCode=200, data=GetStoreInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetStoreInfoResult, tlog, exc)

    @mcp.tool(
        name="list_products",
        description="Get information about all products in a specific e-commerce store",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_products(
        store_id: str = Field(description="The unique ID for the store"),
        count: int = Field(default=10, description="Number of products to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
    ) -> ListProductsResult:
        tlog = ToolLogger(logger, "list_products")

        try:
            client = service.get_service()
            data = client.ecommerce.get_all_store_products(store_id, count=count, offset=offset)
            tlog.success()
            return ListProductsResult(success=True, statusCode=200, data=ListProductsData(**data))
        except Exception as exc:
            return _handle_request_exc(ListProductsResult, tlog, exc)

    @mcp.tool(
        name="get_product_info",
        description="Get detailed information about a specific product in an e-commerce store",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_product_info(
        store_id: str = Field(description="The unique ID for the store"),
        product_id: str = Field(description="The unique ID for the product"),
    ) -> GetProductInfoResult:
        tlog = ToolLogger(logger, "get_product_info")

        try:
            client = service.get_service()
            data = client.ecommerce.get_store_product(store_id, product_id)
            tlog.success()
            return GetProductInfoResult(success=True, statusCode=200, data=GetProductInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetProductInfoResult, tlog, exc)

    @mcp.tool(
        name="list_store_orders",
        description="Get information about all orders in a specific e-commerce store",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_store_orders(
        store_id: str = Field(description="The unique ID for the store"),
        count: int = Field(default=10, description="Number of orders to return (max: 1000)"),
        offset: int = Field(default=0, description="Number of records to skip for pagination"),
        customer_id: Optional[str] = Field(default=None, description="Restrict results to orders made by a specific customer"),
        campaign_id: Optional[str] = Field(default=None, description="Restrict results to orders with a specific campaign ID"),
    ) -> ListStoreOrdersResult:
        tlog = ToolLogger(logger, "list_store_orders")

        query_params = {
            "count": count,
            "offset": offset,
        }
        if customer_id:
            query_params["customer_id"] = customer_id
        if campaign_id:
            query_params["campaign_id"] = campaign_id

        try:
            client = service.get_service()
            data = client.ecommerce.get_store_orders(store_id, **query_params)
            tlog.success()
            return ListStoreOrdersResult(success=True, statusCode=200, data=ListStoreOrdersData(**data))
        except Exception as exc:
            return _handle_request_exc(ListStoreOrdersResult, tlog, exc)

    @mcp.tool(
        name="get_order_info",
        description="Get detailed information about a specific order in an e-commerce store",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_order_info(
        store_id: str = Field(description="The unique ID for the store"),
        order_id: str = Field(description="The unique ID for the order"),
    ) -> GetOrderInfoResult:
        tlog = ToolLogger(logger, "get_order_info")

        try:
            client = service.get_service()
            data = client.ecommerce.get_order(store_id, order_id)
            tlog.success()
            return GetOrderInfoResult(success=True, statusCode=200, data=GetOrderInfoData(**data))
        except Exception as exc:
            return _handle_request_exc(GetOrderInfoResult, tlog, exc)
