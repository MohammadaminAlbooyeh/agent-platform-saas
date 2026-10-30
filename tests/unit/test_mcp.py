"""Unit tests for the MCP tool registry and SSRF protection."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_tools.registry import Registry, Tool  # noqa: E402
from mcp_tools.api_tool import _is_blocked  # noqa: E402


class DummyTool(Tool):
    name = "dummy"
    allowed_plans = ["free"]


def test_registry_register_and_is_allowed():
    reg = Registry()
    reg.register(DummyTool(), plans=["free", "pro"])
    assert reg.is_allowed("dummy", "free") is True
    assert reg.is_allowed("dummy", "pro") is True
    assert reg.is_allowed("dummy", "enterprise") is False


def test_registry_list_tools_by_plan():
    reg = Registry()
    reg.register(DummyTool(), plans=["free"])
    assert reg.list_tools("free") == ["dummy"]
    assert reg.list_tools("pro") == []


def test_ssrf_blocks_private_ips():
    assert _is_blocked("http://127.0.0.1/") is True
    assert _is_blocked("http://10.0.0.1/") is True
    assert _is_blocked("http://192.168.1.1/") is True
    assert _is_blocked("http://169.254.169.254/") is True


def test_ssrf_allows_public_urls():
    assert _is_blocked("https://example.com/") is False
    assert _is_blocked("http://example.com/path") is False
