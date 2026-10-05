"""Coordinator behavior when a scheduled Kibble refresh fails."""

import asyncio
from types import SimpleNamespace

from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.kibble.api import KibbleAuthError, KibbleConnectionError
from custom_components.kibble.coordinator import KibbleCoordinator


def test_failed_refresh_retains_state_and_resets_error_count_on_recovery():
    last_good_state = {"pet": {"id": "pet-1"}, "todaySummary": []}

    class FakeApi:
        fail = True

        async def async_get_state(self):
            if self.fail:
                raise KibbleConnectionError("server unavailable")
            return {"pet": {"id": "pet-1"}, "todaySummary": [{"count": 1}]}

    api = FakeApi()
    coordinator = KibbleCoordinator(None, SimpleNamespace(), api)
    coordinator.data = last_good_state

    retained = asyncio.run(coordinator._async_update_data())

    assert retained is last_good_state
    assert coordinator.consecutive_errors == 1
    assert coordinator.last_error == "KibbleConnectionError: server unavailable"
    assert coordinator.last_error_at is not None

    retained_again = asyncio.run(coordinator._async_update_data())

    assert retained_again is last_good_state
    assert coordinator.consecutive_errors == 2

    api.fail = False
    updated = asyncio.run(coordinator._async_update_data())

    assert updated["todaySummary"] == [{"count": 1}]
    assert coordinator.consecutive_errors == 0
    assert coordinator.last_success_at is not None


def test_initial_connection_failure_has_no_state_to_preserve():
    class FakeApi:
        async def async_get_state(self):
            raise KibbleConnectionError("server unavailable")

    coordinator = KibbleCoordinator(None, SimpleNamespace(), FakeApi())

    try:
        asyncio.run(coordinator._async_update_data())
    except UpdateFailed as err:
        assert str(err) == "server unavailable"
    else:
        raise AssertionError("initial connection failure should fail setup")

    assert coordinator.consecutive_errors == 1


def test_runtime_auth_errors_keep_state_and_start_reauth_once():
    last_good_state = {"pet": {"id": "pet-1"}, "todaySummary": []}
    reauth_calls = []

    class FakeApi:
        async def async_get_state(self):
            raise KibbleAuthError("token rejected")

    entry = SimpleNamespace(
        async_start_reauth=lambda hass: reauth_calls.append(hass),
    )
    hass = object()
    coordinator = KibbleCoordinator(hass, entry, FakeApi())
    coordinator.data = last_good_state

    for expected_count in (1, 2):
        assert asyncio.run(coordinator._async_update_data()) is last_good_state
        assert coordinator.consecutive_errors == expected_count

    assert reauth_calls == [hass]
