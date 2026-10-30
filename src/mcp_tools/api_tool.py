"""API MCP tool with SSRF protection."""

import ipaddress
import urllib.parse

import httpx

from mcp_tools.registry import Tool


# Private/reserved IP ranges that must never be fetched (SSRF protection).
BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def _is_blocked(host: str) -> bool:
    """Return True if the host resolves to a blocked/private network."""
    try:
        info = urllib.parse.urlsplit(host)
        hostname = info.hostname or host
        # Only block literal IP addresses; DNS names are allowed but resolved at request time.
        ip = ipaddress.ip_address(hostname)
        return any(ip in net for net in BLOCKED_NETWORKS)
    except ValueError:
        return False


class APITool(Tool):
    name = "api"
    allowed_plans = ["pro", "enterprise"]

    async def run(self, url: str, tenant_id: str) -> dict:
        """Fetch a URL with SSRF protection."""
        if _is_blocked(url):
            return {
                "tool": "api",
                "tenant_id": tenant_id,
                "url": url,
                "error": "SSRF: blocked address",
            }

        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in ("http", "https"):
            return {
                "tool": "api",
                "tenant_id": tenant_id,
                "url": url,
                "error": "Unsupported scheme",
            }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                return {
                    "tool": "api",
                    "tenant_id": tenant_id,
                    "url": url,
                    "status_code": resp.status_code,
                    "body": resp.text[:5000],
                }
        except Exception as exc:  # noqa: BLE001
            return {
                "tool": "api",
                "tenant_id": tenant_id,
                "url": url,
                "error": str(exc),
            }
