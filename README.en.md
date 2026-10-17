# Kibble Home Assistant Integration (hass-kibble)

<!-- hass-standards:badges:start -->
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat-square)](#installation)
[![Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat-square)](https://github.com/eigger/hass-kibble/releases)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202026.10.2-41BDF5?style=flat-square)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat-square&label=Tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/validate.yml?branch=master&style=flat-square&label=Validate)](https://github.com/eigger/hass-kibble/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat-square)](LICENSE)
<!-- hass-standards:badges:end -->

A **read-only** custom Home Assistant integration for Kibble. It polls the daily summary, individual feeding and care records, overdue medication and reminders every five minutes and exposes them as sensors.

[한국어](README.md)

## Requirements

- Home Assistant **2026.10.2 or newer**, a reachable Kibble server and a pet-bound `state:read` token.
- Local HTTP/HTTPS polling; no Bluetooth adapter or proxy is used.

## Support version change

This change raises the minimum HA version from 2025.3.0 to **2026.10.2**. Upgrade HA before installing a version containing this change. Existing integration settings, pet identifiers and entity IDs are unchanged; you do not need to recreate the integration.

## Installation

1. On Home Assistant 2026.10.2 or newer, add `eigger/hass-kibble` as a custom **Integration** repository in HACS.
2. Install the integration and restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration → Kibble**.
4. Enter the Kibble server URL and a `state:read` API token bound to the pet.

Issue a read-only token for a selected pet from **Kibble → More → API explorer → Integration tokens**. The plaintext is displayed once, immediately after creation, so copy it then.

For manual installation, copy `custom_components/kibble` into the same path under your HA configuration directory and restart. To remove, delete the integration entry, uninstall through HACS or remove that directory, then restart. Update expired tokens through the reauthentication form.

## Supported features and entities

- **Today's events**: Total event count for today. Per-event-type counts and unit-separated totals are available in its `today_summary` attribute.
- **Daily event list**: The `today_events` attribute lists event time, type, offered and consumed amounts, product/preset, note and medication course, newest first. It includes up to 100 events; `today_events_truncated` indicates when more exist.
- **Daily total sensors**: Today's event count, per-event counts, food offered/consumed and water intake are totals that reset at Kibble's today boundary.
- **Current measurement sensors**: Weight shows the latest recorded value; overdue medication and active reminders show their current counts.
- **Overdue medication doses**: Number of medication slots past their scheduled time, with course details.
- **Reminders**: Number of active reminders, with the list as an attribute.
- **Consecutive fetch errors**: A graphable count of consecutive failed requests. The `last_error`, `last_error_at` and `last_success_at` attributes show the latest error and successful fetch times.
- **Refresh now** button: Request an update immediately instead of waiting for the next poll.

Per-event sensors are created from each type's latest event and remain available after a restart at midnight. Care details are available on the Today's events sensor as `medication`, `reminders` and `today_events` attributes. These larger detail attributes are excluded from recorder history to keep the live state within Home Assistant's storage limits; numeric sensors are still recorded normally. Older server responses fall back to the compact `today` totals when possible.

The default update interval is five minutes. A failed request keeps the last successful data and increments the consecutive error count. The count returns to zero after the next successful request. Authentication failures also keep the current data while starting Home Assistant's re-authentication flow. This integration never writes data to Kibble.

## Usage

```yaml
action: button.press
target:
  entity_id: button.bori_refresh_now
```

Select the actual refresh button entity created by your installation.

## Limitations and troubleshooting

This integration is read-only. Add records and change settings in Kibble. After connection failures, inspect the last successful values together with the error count. Check the server address, network access and `state:read` permission; reauthenticate rejected tokens. Remove tokens, private URLs, pet and care details from issue reports. Tests use actual HA with mocked HTTP responses and do not certify a live server.

## Development

The minimum supported and tested HA version is 2026.10.2. Use Python 3.14.2 or newer with the compatible test plugin 0.13.373.

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements_test.txt -r requirements_lint.txt
.venv/bin/python -m pip check
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pytest tests/components/kibble/ -v
```

The current environment also tests the exact minimum because both versions are identical. Tests check that `hacs.json`, the exact HA test requirement and the installed HA version agree. Test dependencies are separate from the runtime manifest; review HA and its compatible plugin together. See [adopted standards](STANDARDS.md) and the [checklist](ADOPTION_CHECKLIST.md) for exact environments and verification limits.

## Support and license

Report issues through [GitHub Issues](https://github.com/eigger/hass-kibble/issues). Licensed under [MIT](LICENSE).
