"""Invoke the refresh action using the actual HA service registry."""


async def test_refresh_button(hass, entry, api_response, entity_id):
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    before = api_response.call_count
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": entity_id("pet-1_refresh", "button")},
        blocking=True,
    )
    await hass.async_block_till_done()
    assert api_response.call_count == before + 1
