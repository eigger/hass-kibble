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
from homeassistant.util import dt as dt_util

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
        self._entry = entry
        self._reauth_started = False
        self.consecutive_errors = 0
        self.last_error: str | None = None
        self.last_error_at: str | None = None
        self.last_success_at: str | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            state = await self._api.async_get_state()
        except KibbleError as err:
            self.consecutive_errors += 1
            self.last_error = (
                f"{type(err).__name__}: {err}"
                if str(err)
                else type(err).__name__
            )
            self.last_error_at = dt_util.utcnow().isoformat()
            _LOGGER.warning(
                "Kibble update failed (%s consecutive failures): %s",
                self.consecutive_errors,
                self.last_error,
            )
            if self.data is not None:
                if isinstance(err, KibbleAuthError) and not self._reauth_started:
                    self._entry.async_start_reauth(self.hass)
                    self._reauth_started = True
                # Returning the cached data keeps coordinator entities available and
                # lets their state continue to show the last successful response.
                return self.data

            # There is no cached state to preserve during the first refresh.
            if isinstance(err, KibbleAuthError):
                raise ConfigEntryAuthFailed(str(err)) from err
            raise UpdateFailed(str(err)) from err

        self.consecutive_errors = 0
        self._reauth_started = False
        self.last_success_at = dt_util.utcnow().isoformat()
        return state
