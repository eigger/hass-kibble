"""Refresh button for Kibble."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KibbleRuntimeData
from .const import DOMAIN
from .coordinator import KibbleCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[KibbleRuntimeData],
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities([KibbleRefreshButton(coordinator, entry)])


class KibbleRefreshButton(CoordinatorEntity[KibbleCoordinator], ButtonEntity):
    """Request an immediate state refresh."""

    _attr_has_entity_name = True
    _attr_translation_key = "refresh"
    _attr_icon = "mdi:refresh"

    def __init__(self, coordinator: KibbleCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        pet = coordinator.data["pet"]
        self._attr_unique_id = f"{entry.unique_id}_refresh"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(pet["id"]))},
            name=str(pet.get("name") or "Kibble"),
            manufacturer="Kibble (self-hosted)",
            model=str(pet.get("species") or "Pet"),
            configuration_url=entry.data.get("url"),
        )

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()
