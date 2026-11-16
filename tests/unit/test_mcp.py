"""Unit tests for the MCP tool registry and SSRF protection."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_tools.registry import Registry, Tool  # noqa: E402
from mcp_tools.api_tool import _is_blocked  # noqa: E402
from mcp_tools.file_tool import FileTool, resolve_safe_path  # noqa: E402
from mcp_tools.database_tool import resolve_query_name  # noqa: E402
import config.settings as settings_module  # noqa: E402


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


def test_ssrf_blocks_hostname_pointing_at_loopback():
    # DNS names that resolve to a private/loopback address must be blocked
    # too, not just literal IPs, or SSRF protection is trivially bypassed.
    assert _is_blocked("http://localhost/") is True


def test_resolve_query_name_maps_free_form_input():
    assert resolve_query_name("invoices please") == "invoices"
    assert resolve_query_name("select 1") == "usage_summary"
    assert resolve_query_name("") == "usage_summary"


def test_file_tool_blocks_path_traversal(tmp_path, monkeypatch):
    monkeypatch.setattr(settings_module.settings, "file_tool_root", str(tmp_path))
    assert resolve_safe_path("tenant-a", "../../etc/passwd") is None


def test_file_tool_reads_within_sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(settings_module.settings, "file_tool_root", str(tmp_path))
    tenant_dir = tmp_path / "tenant-a"
    tenant_dir.mkdir(parents=True, exist_ok=True)
    (tenant_dir / "note.txt").write_text("hello")

    tool = FileTool()
    result = asyncio.run(tool.run(path="note.txt", tenant_id="tenant-a"))
    assert result["exists"] is True
    assert result["content"] == "hello"


def test_file_tool_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(settings_module.settings, "file_tool_root", str(tmp_path))
    tool = FileTool()
    result = asyncio.run(tool.run(path="does-not-exist.txt", tenant_id="tenant-b"))
    assert result["exists"] is False
