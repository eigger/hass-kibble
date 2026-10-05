"""Constants for the Kibble integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "kibble"
CONF_URL = "url"
CONF_API_TOKEN = "api_token"
UPDATE_INTERVAL = timedelta(minutes=5)
