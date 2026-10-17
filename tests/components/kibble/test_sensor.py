"""Read sensors through actual HA states and entity registry."""

from copy import deepcopy

from homeassistant.helpers import entity_registry as er


async def test_platform_states_and_day_boundary(hass, entry, api_response, entity_id):
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    summary = hass.states.get(entity_id("pet-1_daily_summary"))
    assert summary.state == "2"
    assert summary.attributes["state_class"] == "total"
    assert summary.attributes["last_reset"] == "2026-10-04T15:00:00+00:00"
    consumed = hass.states.get(entity_id("pet-1_meal_meal_consumed_g"))
    assert float(consumed.state) == 50
    assert consumed.attributes["state_class"] == "total"
    assert consumed.attributes["last_reset"] == summary.attributes["last_reset"]
    assert hass.states.get(entity_id("pet-1_meal_meal_offered_g")).state == "60.0"
    weight = hass.states.get(entity_id("pet-1_weight_weight_kg"))
    assert weight.state == "unknown"
    assert weight.attributes["state_class"] == "measurement"
    assert "last_reset" not in weight.attributes
    for key in ["overdue_medication", "reminders", "fetch_errors"]:
        value = hass.states.get(entity_id(f"pet-1_{key}"))
        assert value.state == "0"
        assert value.attributes["state_class"] == "measurement"
    # Diagnostic entities are intentionally disabled by default in HA.
    registry = er.async_get(hass)
    assert (
        registry.async_get(entity_id("pet-1_daily_summary")).unique_id
        == "pet-1_daily_summary"
    )


async def test_historical_event_survives_restart_with_zero_count(
    hass, entry, aioclient_mock, state_payload, entity_id
):
    state_payload["todaySummary"] = []
    aioclient_mock.get("http://kibble.test/api/states", json=state_payload)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    meal = hass.states.get(entity_id("pet-1_meal_today"))
    assert meal.state == "0"
    assert meal.attributes["last_occurred_at"] == "2026-10-04T22:00:00Z"


async def test_new_event_type_added_once_and_measurement_recovery(
    hass, entry, api_response, state_payload, entity_id
):
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    updated = deepcopy(state_payload)
    updated["todaySummary"].append({"eventTypeKey": "walk", "count": 3})
    updated["lastEvents"].append(
        {"eventTypeKey": "weight", "quantity": 4.5, "unit": "kg"}
    )
    api_response.clear_requests()
    api_response.get("http://kibble.test/api/states", json=updated)
    await entry.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()
    assert hass.states.get(entity_id("pet-1_walk_today")).state == "3"
    assert hass.states.get(entity_id("pet-1_weight_weight_kg")).state == "4.5"
    await entry.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()
    registry = er.async_get(hass)
    assert (
        sum(e.unique_id == "pet-1_walk_today" for e in registry.entities.values()) == 1
    )
