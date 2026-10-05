# Kibble Home Assistant Integration (hass-kibble)

[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat-square&label=tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![GitHub Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat-square)](https://github.com/eigger/hass-kibble/releases)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat-square)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

A **read-only** custom Home Assistant integration for Kibble. It polls the daily summary, latest events, overdue medication and reminders every five minutes and exposes them as sensors.

## Installation

1. On Home Assistant 2025.3 or newer, add `eigger/hass-kibble` as a custom **Integration** repository in HACS.
2. Install the integration and restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration → Kibble**.
4. Enter the Kibble server URL and a `state:read` API token bound to the pet.

Issue a read-only token for a selected pet from **Kibble → More → API explorer → Integration tokens**. The plaintext is displayed once, immediately after creation, so copy it then.

## Entities

- **Today's events**: Total event count for today. Per-event-type counts and unit-separated totals are available in its `today_summary` attribute.
- **Overdue medication doses**: Number of medication slots past their scheduled time, with course details.
- **Reminders**: Number of active reminders, with the list as an attribute.
- **Refresh now** button: Request an update immediately instead of waiting for the next poll.

Per-event sensors are created from each type's latest event and remain available after a restart at midnight. Detailed state is also available on the Today's events sensor as `today_summary`, `last_events`, `medication` and `reminders` attributes. Older server responses fall back to the compact `today` totals when possible.

The default update interval is five minutes. Authentication failures start Home Assistant's re-authentication flow. This integration never writes data to Kibble.

## Development

```sh
pip install pytest ruff aiohttp
python -m ruff check custom_components/ tests/
python -m pytest tests/ -v
```
