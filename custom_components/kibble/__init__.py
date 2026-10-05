"""Read-only Home Assistant integration for Kibble."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import KibbleApi
from .const import CONF_API_TOKEN, CONF_URL
from .coordinator import KibbleCoordinator

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.SENSOR]


@dataclass
class KibbleRuntimeData:
    """Objects shared by the integration platforms."""

    coordinator: KibbleCoordinator


KibbleConfigEntry = ConfigEntry[KibbleRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: KibbleConfigEntry) -> bool:
    api = KibbleApi(
        async_get_clientsession(hass),
        entry.data[CONF_URL],
        entry.data[CONF_API_TOKEN],
    )
    coordinator = KibbleCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = KibbleRuntimeData(coordinator)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: KibbleConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
