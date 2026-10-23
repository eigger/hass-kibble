"""Kibble entries and the external HTTP response boundary."""

import json
from pathlib import Path

import pytest

# <!-- hass-standards:domain-fixtures:start -->
# Use pytest_homeassistant_custom_component.common.MockConfigEntry for
# mock_config_entry when the integration uses config entries.
# Define mock_client only when an external communication client is present.
# Mock external communication boundaries, never Home Assistant core modules.
# Keep integration-specific fixtures below this managed block.
# <!-- hass-standards:domain-fixtures:end -->
from pytest_homeassistant_custom_component.common import MockConfigEntry


@pytest.fixture
def state_payload():
    return json.loads((Path(__file__).parent / "fixtures/state.json").read_text())


@pytest.fixture
def entry(hass):
    entry = MockConfigEntry(
        domain="kibble",
        title="Bori",
        unique_id="pet-1",
        data={"url": "http://kibble.test", "api_token": "test-token"},
    )
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def api_response(aioclient_mock, state_payload):
    aioclient_mock.get("http://kibble.test/api/states", json=state_payload)
    return aioclient_mock


@pytest.fixture
def entity_id(hass):
    from homeassistant.helpers import entity_registry as er

    def lookup(unique_id, domain="sensor"):
        result = er.async_get(hass).async_get_entity_id(domain, "kibble", unique_id)
        assert result is not None
        return result

    return lookup
