"""Sensors for Kibble's daily summary and care state."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KibbleRuntimeData
from .const import DOMAIN
from .coordinator import KibbleCoordinator

_EVENT_TYPE_KEYS = {
    "care",
    "meal",
    "medication",
    "note",
    "observation",
    "pee",
    "play",
    "poop",
    "remedy",
    "supplement",
    "symptom",
    "temperature",
    "treat",
    "vaccination",
    "vet_visit",
    "vomit",
    "walk",
    "water",
    "weight",
}

_EVENT_TYPE_ICONS = {
    "care": "mdi:hand-heart",
    "meal": "mdi:food",
    "medication": "mdi:pill",
    "note": "mdi:note-text",
    "observation": "mdi:eye",
    "pee": "mdi:water-outline",
    "play": "mdi:toy-brick",
    "poop": "mdi:emoticon-poop",
    "remedy": "mdi:pill",
    "supplement": "mdi:flask",
    "symptom": "mdi:heart-pulse",
    "temperature": "mdi:thermometer",
    "treat": "mdi:cookie",
    "vaccination": "mdi:needle",
    "vet_visit": "mdi:stethoscope",
    "vomit": "mdi:emoticon-sick",
    "walk": "mdi:walk",
    "water": "mdi:water",
    "weight": "mdi:scale",
}

_MEASUREMENTS = (
    # event key, metric key, field, default unit, icon, is latest-value metric
    ("meal", "meal_offered", "quantityOffered", "g", "mdi:food", False),
    ("meal", "meal_consumed", "quantity", "g", "mdi:food", False),
    ("water", "water_intake", "quantity", "ml", "mdi:water", False),
    ("weight", "weight", "lastQuantity", "kg", "mdi:scale", True),
)


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
        KibbleFetchErrorSensor(coordinator, entry),
    ]
    known_keys: set[str] = set()
    entities.extend(_new_event_sensors(coordinator, entry, pet_id, state, known_keys))
    known_measurements: set[str] = set()
    entities.extend(
        _new_measurement_sensors(
            coordinator, entry, pet_id, state, known_measurements
        )
    )
    async_add_entities(entities)

    @callback
    def add_new_event_type_sensors() -> None:
        new_entities = _new_event_sensors(
            coordinator, entry, pet_id, coordinator.data or {}, known_keys
        )
        new_entities.extend(
            _new_measurement_sensors(
                coordinator,
                entry,
                pet_id,
                coordinator.data or {},
                known_measurements,
            )
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


def _new_measurement_sensors(
    coordinator: KibbleCoordinator,
    entry: ConfigEntry,
    pet_id: str,
    state: dict[str, Any],
    known_measurements: set[str],
) -> list[SensorEntity]:
    """Create stable, unit-specific sensors for food, water, and weight values."""
    entities: list[SensorEntity] = []
    rows = list(state.get("todaySummary", []))
    rows.extend(state.get("lastEvents", []))
    for event_key, metric_key, field, default_unit, icon, is_latest in _MEASUREMENTS:
        units = {default_unit}
        for row in rows:
            if row.get("eventTypeKey") != event_key:
                continue
            row_unit = row.get("lastQuantityUnit") or row.get("unit") or row.get("defaultUnit")
            if row_unit:
                units.add(str(row_unit))
            for total in row.get("totals", []):
                unit = total.get("unit") or row.get("defaultUnit") or default_unit
                if unit:
                    units.add(str(unit))
        for unit in units:
            key = f"{event_key}:{metric_key}:{unit}"
            if key in known_measurements:
                continue
            known_measurements.add(key)
            entities.append(
                KibbleMeasurementSensor(
                    coordinator,
                    entry,
                    pet_id,
                    event_key,
                    metric_key,
                    field,
                    unit,
                    icon,
                    is_latest,
                )
            )
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

    _unrecorded_attributes = frozenset(
        {"today_summary", "today_events", "last_events", "medication", "reminders"}
    )
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
            "today_events": state.get("todayEvents", []),
            "today_events_truncated": state.get("todayEventsTruncated", False),
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
    _attr_icon = "mdi:pill"
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


class KibbleFetchErrorSensor(KibbleCoordinatorSensor):
    """Consecutive polling failures and details about the latest fetch error."""

    _attr_translation_key = "fetch_errors"
    _attr_icon = "mdi:cloud-alert-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: KibbleCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_fetch_errors"

    @property
    def native_value(self) -> int:
        return self.coordinator.consecutive_errors

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "last_error": self.coordinator.last_error,
            "last_error_at": self.coordinator.last_error_at,
            "last_success_at": self.coordinator.last_success_at,
        }


class KibbleEventTypeSensor(KibbleCoordinatorSensor):
    """One sensor per event type that has recorded history."""

    def __init__(
        self,
        coordinator: KibbleCoordinator,
        entry: ConfigEntry,
        pet_id: str,
        row: dict[str, Any],
    ) -> None:
        super().__init__(coordinator, entry)
        self._event_type_key = str(row["eventTypeKey"])
        if self._event_type_key in _EVENT_TYPE_KEYS:
            self._attr_translation_key = f"event_type_{self._event_type_key}"
        else:
            label = row.get("label")
            if label and not str(label).startswith("eventType."):
                self._attr_name = str(label)
            else:
                fallback = str(label or self._event_type_key).removeprefix("eventType.")
                self._attr_name = fallback.replace("_", " ").title()
        self._attr_icon = _EVENT_TYPE_ICONS.get(self._event_type_key, "mdi:paw")
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


class KibbleMeasurementSensor(KibbleCoordinatorSensor):
    """A unit-specific daily amount or latest measurement sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: KibbleCoordinator,
        entry: ConfigEntry,
        pet_id: str,
        event_type_key: str,
        metric_key: str,
        field: str,
        unit: str,
        icon: str,
        is_latest: bool,
    ) -> None:
        super().__init__(coordinator, entry)
        self._event_type_key = event_type_key
        self._field = field
        self._unit = unit
        self._is_latest = is_latest
        self._attr_translation_key = metric_key
        self._attr_translation_placeholders = {"unit": unit}
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_unique_id = f"{pet_id}_{event_type_key}_{metric_key}_{unit}"

    @property
    def _summary_row(self) -> dict[str, Any] | None:
        return next(
            (
                row
                for row in self.coordinator.data.get("todaySummary", [])
                if row.get("eventTypeKey") == self._event_type_key
            ),
            None,
        )

    @property
    def _last_event(self) -> dict[str, Any] | None:
        return next(
            (
                row
                for row in self.coordinator.data.get("lastEvents", [])
                if row.get("eventTypeKey") == self._event_type_key
            ),
            None,
        )

    @property
    def native_value(self) -> int | float | None:
        if self._is_latest:
            summary = self._summary_row or {}
            last_event = self._last_event or {}
            candidates = (
                (
                    summary.get(self._field),
                    summary.get("lastQuantityUnit") or summary.get("defaultUnit"),
                ),
                (last_event.get("quantity"), last_event.get("unit")),
            )
            for value, unit in candidates:
                if (
                    isinstance(value, (int, float))
                    and str(unit or self._unit) == self._unit
                ):
                    return value
            return None

        total = 0.0
        has_unknown_amount = False
        for row in self.coordinator.data.get("todaySummary", []):
            if row.get("eventTypeKey") != self._event_type_key:
                continue
            unit_totals = row.get("totals", [])
            if not unit_totals and row.get("count", 0) > 0:
                return None
            for unit_total in unit_totals:
                unit = unit_total.get("unit") or row.get("defaultUnit") or self._unit
                if str(unit) != self._unit:
                    continue
                value = unit_total.get(self._field)
                if isinstance(value, (int, float)):
                    total += value
                else:
                    has_unknown_amount = True
        return None if has_unknown_amount else total

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        row = self._summary_row or self._last_event or {}
        return {
            "event_type_key": self._event_type_key,
            "last_occurred_at": row.get("lastOccurredAt") or row.get("occurredAt"),
            "unit": self._unit,
        }
