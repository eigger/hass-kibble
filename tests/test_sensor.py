"""Sensor recovery behavior across a Kibble day boundary."""

from types import SimpleNamespace

from custom_components.kibble.sensor import (
    KibbleDailySummarySensor,
    KibbleEventTypeSensor,
    KibbleFetchErrorSensor,
    KibbleMeasurementSensor,
    _new_event_sensors,
)


def _runtime(state):
    coordinator = SimpleNamespace(data=state)
    entry = SimpleNamespace(unique_id="pet-1", data={"url": "http://kibble"})
    return coordinator, entry


def test_historical_event_types_restore_with_zero_today_count_after_restart():
    state = {
        "pet": {"id": "pet-1", "name": "Bori", "species": "DOG"},
        "todaySummary": [],
        "lastEvents": [
            {
                "eventTypeKey": "meal",
                "label": "Meal",
                "occurredAt": "2026-10-04T22:00:00Z",
                "quantity": 30,
                "unit": "g",
                "scaleValue": None,
            }
        ],
    }
    coordinator, entry = _runtime(state)
    known_keys: set[str] = set()

    entities = _new_event_sensors(coordinator, entry, "pet-1", state, known_keys)

    assert len(entities) == 1
    assert isinstance(entities[0], KibbleEventTypeSensor)
    assert entities[0].native_value == 0
    assert entities[0].extra_state_attributes["last_occurred_at"] == (
        "2026-10-04T22:00:00Z"
    )


def test_daily_sensor_sums_today_summary_rows():
    state = {
        "pet": {"id": "pet-1", "name": "Bori", "species": "DOG"},
        "todaySummary": [
            {"eventTypeKey": "meal", "count": 2},
            {"eventTypeKey": "water", "count": 3},
        ],
        "lastEvents": [],
    }
    coordinator, entry = _runtime(state)
    sensor = KibbleDailySummarySensor(coordinator, entry)

    assert sensor.native_value == 5
    assert sensor._attr_state_class == "total"


def test_daily_totals_use_kibble_day_boundary_as_last_reset():
    state = {
        "pet": {"id": "pet-1", "name": "Bori", "species": "DOG"},
        "todaySince": "2026-10-04T15:00:00+00:00",
        "todaySummary": [{"eventTypeKey": "meal", "count": 2}],
        "lastEvents": [],
    }
    coordinator, entry = _runtime(state)

    summary = KibbleDailySummarySensor(coordinator, entry)
    event_count = KibbleEventTypeSensor(
        coordinator, entry, "pet-1", {"eventTypeKey": "meal"}
    )
    consumed = KibbleMeasurementSensor(
        coordinator,
        entry,
        "pet-1",
        "meal",
        "meal_consumed",
        "quantity",
        "g",
        "mdi:food",
        False,
    )

    expected_reset = "2026-10-04T15:00:00+00:00"
    assert summary.last_reset.isoformat() == expected_reset
    assert event_count._attr_state_class == "total"
    assert event_count.last_reset.isoformat() == expected_reset
    assert consumed._attr_state_class == "total"
    assert consumed.last_reset.isoformat() == expected_reset


def test_latest_weight_uses_measurement_state_class_without_daily_reset():
    state = {
        "pet": {"id": "pet-1", "name": "Bori", "species": "DOG"},
        "todaySince": "2026-10-04T15:00:00+00:00",
        "todaySummary": [],
        "lastEvents": [],
    }
    coordinator, entry = _runtime(state)
    weight = KibbleMeasurementSensor(
        coordinator,
        entry,
        "pet-1",
        "weight",
        "weight",
        "lastQuantity",
        "kg",
        "mdi:scale",
        True,
    )

    assert weight._attr_state_class == "measurement"
    assert weight.last_reset is None


def test_fetch_error_sensor_exposes_count_and_latest_error_details():
    coordinator = SimpleNamespace(
        data={"pet": {"id": "pet-1", "name": "Bori"}},
        consecutive_errors=2,
        last_error="TimeoutError",
        last_error_at="2026-10-05T13:00:00+00:00",
        last_success_at="2026-10-05T12:55:00+00:00",
    )
    entry = SimpleNamespace(unique_id="pet-1", data={"url": "http://kibble"})

    sensor = KibbleFetchErrorSensor(coordinator, entry)

    assert sensor.native_value == 2
    assert sensor.extra_state_attributes == {
        "last_error": "TimeoutError",
        "last_error_at": "2026-10-05T13:00:00+00:00",
        "last_success_at": "2026-10-05T12:55:00+00:00",
    }
