"""Validate citation URL syntax without contacting the source."""
import ipaddress
from urllib.parse import urlsplit


def valid_source_url(value: str) -> bool:
    if not isinstance(value, str) or not value or value.strip() != value:
        return False
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value):
        return False
    try:
        url = urlsplit(value)
        host, port = url.hostname, url.port
    except ValueError:
        return False
    if url.scheme not in ("http", "https") or not host:
        return False
    if url.username is not None or url.password is not None or url.netloc.endswith(":"):
        return False
    if port == 0:
        return False
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return "." in host and host != "localhost" and not host.endswith(".localhost")
    return ip.is_global
