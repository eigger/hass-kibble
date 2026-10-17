"""Keep last good state on failure and recover through real HA updates."""


async def test_failures_preserve_state_and_recover(
    hass, entry, api_response, entity_id, caplog
):
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    coordinator = entry.runtime_data.coordinator
    last_good = coordinator.data
    for failures in (1, 2):
        api_response.clear_requests()
        api_response.get("http://kibble.test/api/states", status=500)
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        assert coordinator.data is last_good
        assert coordinator.consecutive_errors == failures
        assert coordinator.last_error.startswith("KibbleConnectionError:")
        assert coordinator.last_error_at is not None
        assert hass.states.get(entity_id("pet-1_daily_summary")).state == "2"
        assert hass.states.get(entity_id("pet-1_fetch_errors")).state == str(failures)
    api_response.clear_requests()
    api_response.get("http://kibble.test/api/states", json=last_good)
    await coordinator.async_refresh()
    await hass.async_block_till_done()
    assert coordinator.consecutive_errors == 0
    assert coordinator.last_success_at is not None
    assert hass.states.get(entity_id("pet-1_fetch_errors")).state == "0"
    assert (
        sum(
            record.levelname == "WARNING" and "Kibble update failed" in record.message
            for record in caplog.records
        )
        == 1
    )


async def test_runtime_auth_starts_only_one_reauth(hass, entry, api_response):
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    coordinator = entry.runtime_data.coordinator
    last_good = coordinator.data
    api_response.clear_requests()
    api_response.get("http://kibble.test/api/states", status=401)
    for _ in range(2):
        await coordinator.async_refresh()
        await hass.async_block_till_done()
    assert coordinator.data is last_good
    assert coordinator.consecutive_errors == 2
    assert len(hass.config_entries.flow.async_progress()) == 1
