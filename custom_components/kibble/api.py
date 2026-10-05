"""Async client for Kibble's read-only state API."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit, urlunsplit

from aiohttp import ClientError, ClientSession, ClientTimeout


class KibbleError(Exception):
    """Base error for Kibble API failures."""


class KibbleAuthError(KibbleError):
    """The API token is invalid or lacks the state:read scope."""


class KibbleConnectionError(KibbleError):
    """Kibble could not be reached or returned an invalid response."""


def normalize_url(url: str) -> str:
    """Normalize a Kibble base URL without discarding reverse-proxy paths."""
    value = url.strip().rstrip("/")
    if not value:
        raise ValueError("Kibble URL is required")
    parts = urlsplit(value if "://" in value else f"http://{value}")
    if not parts.netloc or parts.scheme not in ("http", "https"):
        raise ValueError("Kibble URL must use HTTP or HTTPS")
    return urlunsplit((parts.scheme, parts.netloc, parts.path.rstrip("/"), "", ""))


class KibbleApi:
    """Thin wrapper around ``GET /api/states``."""

    def __init__(self, session: ClientSession, url: str, api_token: str) -> None:
        self._session = session
        self._url = normalize_url(url)
        self._api_token = api_token.strip()

    async def async_get_state(self) -> dict[str, Any]:
        """Fetch state for the pet selected by the API token."""
        url = f"{self._url}/api/states"
        try:
            async with self._session.get(
                url,
                headers={"Authorization": f"Bearer {self._api_token}"},
                timeout=ClientTimeout(total=15),
            ) as response:
                if response.status in (401, 403):
                    raise KibbleAuthError(
                        "Kibble rejected the token or it lacks state:read"
                    )
                response.raise_for_status()
                payload = await response.json()
        except KibbleAuthError:
            raise
        except (ClientError, ValueError, TimeoutError) as err:
            raise KibbleConnectionError(f"Kibble request failed: {err}") from err

        if not isinstance(payload, dict) or not isinstance(payload.get("pet"), dict):
            raise KibbleConnectionError("Kibble returned an invalid state response")
        if not payload["pet"].get("id"):
            raise KibbleConnectionError("Kibble response does not identify a pet")

        # Older Kibble servers expose `today` but not its richer `todaySummary`.
        # Preserve useful counts and quantities while remaining compatible.
        if not isinstance(payload.get("todaySummary"), list):
            today = payload.get("today", [])
            if not isinstance(today, list):
                today = []
            payload["todaySummary"] = [
                {
                    "eventTypeKey": row.get("eventTypeKey"),
                    "label": row.get("label"),
                    "category": None,
                    "scaleType": None,
                    "defaultUnit": row.get("unit"),
                    "count": row.get("count", 0),
                    "totals": (
                        [
                            {
                                "unit": row.get("unit"),
                                "count": row.get("count", 0),
                                "quantity": row.get("total"),
                                "quantityOffered": None,
                            }
                        ]
                        if row.get("total") is not None
                        else []
                    ),
                    "lastOccurredAt": None,
                    "lastScaleValue": None,
                    "lastQuantity": None,
                    "lastQuantityUnit": None,
                }
                for row in today
                if isinstance(row, dict) and row.get("eventTypeKey")
            ]
        else:
            payload["todaySummary"] = [
                row for row in payload["todaySummary"] if isinstance(row, dict)
            ]
        if not isinstance(payload.get("lastEvents"), list):
            payload["lastEvents"] = []
        else:
            payload["lastEvents"] = [
                row for row in payload["lastEvents"] if isinstance(row, dict)
            ]
        return payload
