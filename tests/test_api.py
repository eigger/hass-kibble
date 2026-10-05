"""Tests for the Kibble API client."""

import asyncio

import pytest
from aiohttp import ClientError

from custom_components.kibble.api import (
    KibbleApi,
    KibbleAuthError,
    KibbleConnectionError,
    normalize_url,
)


class FakeResponse:
    def __init__(self, status=200, json_data=None, error=None):
        self.status = status
        self._json = json_data
        self._error = error

    async def __aenter__(self):
        if self._error:
            raise self._error
        return self

    async def __aexit__(self, *exc_info):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise ClientError(f"HTTP {self.status}")

    async def json(self):
        return self._json


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.url = None
        self.headers = None
        self.timeout = None

    def get(self, url, headers=None, timeout=None):
        self.url = url
        self.headers = headers
        self.timeout = timeout
        return self.response


def run(coro):
    return asyncio.run(coro)


def test_normalize_url_preserves_reverse_proxy_prefix():
    assert normalize_url(" https://kibble.example/prefix/ ") == (
        "https://kibble.example/prefix"
    )


def test_normalize_url_adds_http_for_local_host():
    assert normalize_url("kibble.local:8080/") == "http://kibble.local:8080"


def test_normalize_url_rejects_non_http_scheme():
    with pytest.raises(ValueError):
        normalize_url("ftp://kibble.example")


def test_get_state_sends_bearer_and_returns_pet_state():
    expected = {
        "pet": {"id": "pet-1", "name": "Bori"},
        "todaySummary": [{"eventTypeKey": "meal", "count": 2}],
    }
    session = FakeSession(FakeResponse(json_data=expected))
    api = KibbleApi(session, "https://kibble.example/", " kbl_test ")

    result = run(api.async_get_state())

    assert result == expected
    assert session.url == "https://kibble.example/api/states"
    assert session.headers == {"Authorization": "Bearer kbl_test"}
    assert session.timeout.total == 15


def test_old_server_today_shape_is_adapted_to_today_summary():
    response = {
        "pet": {"id": "pet-1", "name": "Bori"},
        "today": [
            {
                "eventTypeKey": "meal",
                "label": "Meal",
                "count": 2,
                "total": 60,
                "unit": "g",
            }
        ],
    }
    api = KibbleApi(
        FakeSession(FakeResponse(json_data=response)), "http://kibble", "token"
    )

    result = run(api.async_get_state())

    assert result["todaySummary"][0]["eventTypeKey"] == "meal"
    assert result["todaySummary"][0]["totals"] == [
        {"unit": "g", "count": 2, "quantity": 60, "quantityOffered": None}
    ]


@pytest.mark.parametrize("status", [401, 403])
def test_auth_and_missing_scope_are_auth_errors(status):
    api = KibbleApi(FakeSession(FakeResponse(status=status)), "http://kibble", "bad")
    with pytest.raises(KibbleAuthError):
        run(api.async_get_state())


def test_connection_errors_are_wrapped():
    api = KibbleApi(
        FakeSession(FakeResponse(error=ClientError("offline"))),
        "http://kibble",
        "token",
    )
    with pytest.raises(KibbleConnectionError):
        run(api.async_get_state())


def test_request_timeout_is_wrapped_as_connection_error():
    api = KibbleApi(
        FakeSession(FakeResponse(error=TimeoutError("timed out"))),
        "http://kibble",
        "token",
    )
    with pytest.raises(KibbleConnectionError, match="timed out"):
        run(api.async_get_state())


def test_empty_request_timeout_still_reports_timeout_type():
    api = KibbleApi(
        FakeSession(FakeResponse(error=TimeoutError())),
        "http://kibble",
        "token",
    )
    with pytest.raises(KibbleConnectionError, match="TimeoutError"):
        run(api.async_get_state())


@pytest.mark.parametrize("payload", [None, [], {}, {"pet": {}}])
def test_invalid_state_payload_is_rejected(payload):
    api = KibbleApi(
        FakeSession(FakeResponse(json_data=payload)), "http://kibble", "token"
    )
    with pytest.raises(KibbleConnectionError):
        run(api.async_get_state())
