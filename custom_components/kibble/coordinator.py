"""Poll Kibble state for the configured pet."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import KibbleApi, KibbleAuthError, KibbleError
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class KibbleCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch the current state and daily summary every five minutes."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, api: KibbleApi) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN} state",
            update_interval=UPDATE_INTERVAL,
        )
        self._api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self._api.async_get_state()
        except KibbleAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except KibbleError as err:
            raise UpdateFailed(str(err)) from err
