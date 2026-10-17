"""Exercise actual config entry setup, reload, cleanup and retry."""

from homeassistant.config_entries import ConfigEntryState


async def test_setup_reload_and_unload(hass, entry, api_response, entity_id):
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    coordinator = entry.runtime_data.coordinator
    assert hass.states.get(entity_id("pet-1_daily_summary")).state == "2"
    assert coordinator._listeners
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.runtime_data.coordinator is not coordinator
    assert not coordinator._listeners
    current = entry.runtime_data.coordinator
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED
    assert not current._listeners
    assert current._unsub_refresh is None
    assert hass.states.get(entity_id("pet-1_daily_summary")).state == "unavailable"


async def test_connection_failure_then_retry(
    hass, entry, aioclient_mock, state_payload
):
    aioclient_mock.get("http://kibble.test/api/states", status=500)
    assert not await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY
    aioclient_mock.clear_requests()
    aioclient_mock.get("http://kibble.test/api/states", json=state_payload)
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED


async def test_initial_auth_failure(hass, entry, aioclient_mock):
    aioclient_mock.get("http://kibble.test/api/states", status=401)
    assert not await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert any(
        flow["context"].get("source") == "reauth"
        for flow in hass.config_entries.flow.async_progress()
    )
