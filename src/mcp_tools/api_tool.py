"""API MCP tool with SSRF protection."""

import ipaddress
import socket
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
    """Return True if `host` is, or resolves to, a blocked/private network address.

    A hostname that only resolves to a private/loopback/link-local address (e.g.
    an attacker-controlled DNS name pointed at 127.0.0.1 or a cloud metadata IP)
    is blocked too, not just literal IPs — otherwise SSRF protection is trivially
    bypassed by fetching through DNS instead of an IP literal.
    """
    try:
        info = urllib.parse.urlsplit(host)
        hostname = info.hostname or host
    except ValueError:
        return True  # unparsable host; block defensively

    try:
        ip = ipaddress.ip_address(hostname)
        return any(ip in net for net in BLOCKED_NETWORKS)
    except ValueError:
        pass  # not a literal IP; resolve it below

    try:
        resolved_ips = {addr[4][0] for addr in socket.getaddrinfo(hostname, None)}
    except socket.gaierror:
        return True  # cannot resolve; block defensively

    for addr in resolved_ips:
        try:
            ip = ipaddress.ip_address(addr)
        except ValueError:
            continue
        if any(ip in net for net in BLOCKED_NETWORKS):
            return True
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
