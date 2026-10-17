# User guide and troubleshooting

[English](user-guide.md) | [한국어](ko/user-guide.md) | [README](../README.md)

## Requirements

- Home Assistant **2025.3.0 or newer**, a reachable Kibble server and a pet-bound `state:read` token.
- Local HTTP/HTTPS polling; no Bluetooth adapter or proxy is used.

## Installation

1. On Home Assistant 2025.3.0 or newer, add `eigger/hass-kibble` as a custom **Integration** repository in HACS.
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

## Usage badge

The Usage badge reports installations participating in Home Assistant Analytics, rather than all installations. It stays linked to the live data even when this integration has no published count yet; an unavailable value does not mean zero installations.
