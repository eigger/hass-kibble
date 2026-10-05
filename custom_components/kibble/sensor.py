"""Sensors for Kibble's daily summary and care state."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KibbleRuntimeData
from .const import DOMAIN
from .coordinator import KibbleCoordinator


def _device_info(entry: ConfigEntry, state: dict[str, Any]) -> DeviceInfo:
    pet = state["pet"]
    return DeviceInfo(
        identifiers={(DOMAIN, str(pet["id"]))},
        name=str(pet.get("name") or "Kibble"),
        manufacturer="Kibble (self-hosted)",
        model=str(pet.get("species") or "Pet"),
        configuration_url=entry.data.get("url"),
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[KibbleRuntimeData],
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    state = coordinator.data or {}
    pet_id = str(state.get("pet", {}).get("id", entry.unique_id))
    entities: list[SensorEntity] = [
        KibbleDailySummarySensor(coordinator, entry),
        KibbleOverdueMedicationSensor(coordinator, entry),
        KibbleReminderSensor(coordinator, entry),
    ]
    known_keys: set[str] = set()
    entities.extend(_new_event_sensors(coordinator, entry, pet_id, state, known_keys))
    async_add_entities(entities)

    @callback
    def add_new_event_type_sensors() -> None:
        new_entities = _new_event_sensors(
            coordinator, entry, pet_id, coordinator.data or {}, known_keys
        )
        if new_entities:
            async_add_entities(new_entities)

    entry.async_on_unload(coordinator.async_add_listener(add_new_event_type_sensors))


def _new_event_sensors(
    coordinator: KibbleCoordinator,
    entry: ConfigEntry,
    pet_id: str,
    state: dict[str, Any],
    known_keys: set[str],
) -> list[SensorEntity]:
    """Create a sensor the first time a new event type appears in today's summary."""
    entities: list[SensorEntity] = []
    rows = list(state.get("todaySummary", []))
    for event in state.get("lastEvents", []):
        if not any(
            row.get("eventTypeKey") == event.get("eventTypeKey") for row in rows
        ):
            rows.append(event)
    for row in rows:
        if not isinstance(row, dict) or not row.get("eventTypeKey"):
            continue
        key = str(row["eventTypeKey"])
        if key in known_keys:
            continue
        known_keys.add(key)
        entities.append(KibbleEventTypeSensor(coordinator, entry, pet_id, row))
    return entities


class KibbleCoordinatorSensor(CoordinatorEntity[KibbleCoordinator], SensorEntity):
    """Base sensor bound to the selected Kibble pet."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: KibbleCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._pet_id = str(coordinator.data["pet"]["id"])
        self._attr_device_info = _device_info(entry, coordinator.data)


class KibbleDailySummarySensor(KibbleCoordinatorSensor):
    """Daily total event count with the full state attached as attributes."""

    _attr_translation_key = "daily_summary"
    _attr_icon = "mdi:clipboard-text-clock-outline"

    def __init__(self, coordinator: KibbleCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_daily_summary"

    @property
    def native_value(self) -> int:
        return sum(int(row.get("count", 0)) for row in self._today_summary)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        state = self.coordinator.data
        return {
            "pet": state.get("pet"),
            "generated_at": state.get("generatedAt"),
            "today_since": state.get("todaySince"),
            "today_summary": self._today_summary,
            "last_events": state.get("lastEvents", []),
            "medication": state.get("medication", {}),
            "reminders": state.get("reminders", []),
        }

    @property
    def _today_summary(self) -> list[dict[str, Any]]:
        return self.coordinator.data.get("todaySummary", [])


class KibbleOverdueMedicationSensor(KibbleCoordinatorSensor):
    """Number of medication doses whose scheduled time has passed."""

    _attr_translation_key = "overdue_medication"
    _attr_icon = "mdi:pill-clock"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: KibbleCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_overdue_medication"

    @property
    def native_value(self) -> int:
        medication = self.coordinator.data.get("medication", {})
        return len(medication.get("overdueDoses", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.coordinator.data.get("medication", {})


class KibbleReminderSensor(KibbleCoordinatorSensor):
    """Number of active reminders, with their details as attributes."""

    _attr_translation_key = "reminders"
    _attr_icon = "mdi:bell-outline"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: KibbleCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_reminders"

    @property
    def native_value(self) -> int:
        return len(self.coordinator.data.get("reminders", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"items": self.coordinator.data.get("reminders", [])}


class KibbleEventTypeSensor(KibbleCoordinatorSensor):
    """One sensor per event type that has recorded history."""

    _attr_icon = "mdi:paw"

    def __init__(
        self,
        coordinator: KibbleCoordinator,
        entry: ConfigEntry,
        pet_id: str,
        row: dict[str, Any],
    ) -> None:
        super().__init__(coordinator, entry)
        self._event_type_key = str(row["eventTypeKey"])
        self._attr_name = str(row.get("label") or self._event_type_key)
        self._attr_unique_id = f"{pet_id}_{self._event_type_key}_today"

    @property
    def _row(self) -> dict[str, Any]:
        state = self.coordinator.data
        today = next(
            (
                row
                for row in state.get("todaySummary", [])
                if row.get("eventTypeKey") == self._event_type_key
            ),
            None,
        )
        if today is not None:
            return today
        last = next(
            (
                row
                for row in state.get("lastEvents", [])
                if row.get("eventTypeKey") == self._event_type_key
            ),
            {},
        )
        return {
            "count": 0,
            "totals": [],
            "lastOccurredAt": last.get("occurredAt"),
            "lastScaleValue": last.get("scaleValue"),
            "lastQuantity": last.get("quantity"),
            "lastQuantityUnit": last.get("unit"),
        }

    @property
    def native_value(self) -> int:
        return int(self._row.get("count", 0))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        row = self._row
        return {
            "event_type_key": self._event_type_key,
            "category": row.get("category"),
            "totals": row.get("totals", []),
            "last_occurred_at": row.get("lastOccurredAt"),
            "last_scale_value": row.get("lastScaleValue"),
            "last_quantity": row.get("lastQuantity"),
            "last_quantity_unit": row.get("lastQuantityUnit"),
        }
