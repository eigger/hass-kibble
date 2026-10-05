"""Config flow for the Kibble integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    KibbleApi,
    KibbleAuthError,
    KibbleConnectionError,
    KibbleError,
    normalize_url,
)
from .const import CONF_API_TOKEN, CONF_URL, DOMAIN


class KibbleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up a read-only connection to one Kibble pet."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            url = user_input[CONF_URL]
            api_token = user_input[CONF_API_TOKEN].strip()
            try:
                url = normalize_url(url)
                api = KibbleApi(async_get_clientsession(self.hass), url, api_token)
                state = await api.async_get_state()
            except KibbleAuthError:
                errors["base"] = "invalid_auth"
            except KibbleConnectionError:
                errors["base"] = "cannot_connect"
            except (KibbleError, ValueError):
                errors["base"] = "unknown"
            else:
                pet = state["pet"]
                await self.async_set_unique_id(str(pet["id"]))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=str(pet.get("name") or "Kibble"),
                    data={CONF_URL: url, CONF_API_TOKEN: api_token},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL): str,
                    vol.Required(CONF_API_TOKEN): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            token = user_input[CONF_API_TOKEN].strip()
            api = KibbleApi(
                async_get_clientsession(self.hass), entry.data[CONF_URL], token
            )
            try:
                state = await api.async_get_state()
            except KibbleAuthError:
                errors["base"] = "invalid_auth"
            except KibbleConnectionError:
                errors["base"] = "cannot_connect"
            except KibbleError:
                errors["base"] = "unknown"
            else:
                if str(state["pet"]["id"]) != entry.unique_id:
                    errors["base"] = "wrong_pet"
                else:
                    return self.async_update_reload_and_abort(
                        entry, data_updates={CONF_API_TOKEN: token}
                    )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_API_TOKEN): str}),
            errors=errors,
        )
