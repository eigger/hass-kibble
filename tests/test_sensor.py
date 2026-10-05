"""Sensor recovery behavior across a Kibble day boundary."""

from types import SimpleNamespace

from custom_components.kibble.sensor import (
    KibbleDailySummarySensor,
    KibbleEventTypeSensor,
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
