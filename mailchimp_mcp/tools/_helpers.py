"""Shared error helpers for all tool modules."""

from mailchimp_marketing.api_client import ApiClientError

from ..logging_utils import ToolLogger
from ..schemas import ToolError


def _err(result_class, tlog, code, message, status, retriable=False, retry_after=None):
    tlog.failure(code, message)
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _handle_request_exc(result_class, tlog, exc):
    if isinstance(exc, ApiClientError):
        status = exc.status_code if exc.status_code is not None else 502
        return _upstream_err(result_class, tlog, status, exc)
    if isinstance(exc, ValueError):
        tlog.failure("AUTH_ERROR", str(exc))
        return result_class(success=False, statusCode=401, retriable=False,
            error=ToolError(code="AUTH_ERROR", message=str(exc)))
    tlog.failure("SERVER_ERROR", str(exc))
    return result_class(success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message=str(exc)))


def _upstream_err(result_class, tlog, status, exc, retry_after=None):
    retriable = status in (429, 500, 502, 503)
    tlog.failure("UPSTREAM_ERROR", f"HTTP {status}")
    msg = exc.text if hasattr(exc, "text") and exc.text else f"HTTP {status}"
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code="UPSTREAM_ERROR", message=str(msg)),
    )
