# Kibble Home Assistant Integration (hass-kibble)

<!-- hass-standards:badges:start -->
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat-square)](#installation)
[![Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat-square)](https://github.com/eigger/hass-kibble/releases)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.3.0-41BDF5?style=flat-square)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat-square&label=Tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/validate.yml?branch=master&style=flat-square&label=Validate)](https://github.com/eigger/hass-kibble/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat-square)](LICENSE)
[![Analytics reporting installs](https://img.shields.io/badge/dynamic/json?style=flat-square&color=41BDF5&label=Usage&query=%24.kibble.total&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json)](https://analytics.home-assistant.io/)
<!-- hass-standards:badges:end -->

A **read-only** custom Home Assistant integration for Kibble. It polls the daily summary, individual feeding and care records, overdue medication and reminders every five minutes and exposes them as sensors.

[English](README.md) | [한국어](README.ko.md)

## Features

- Sensors for daily feeding and care records, overdue medication and reminders
- Daily totals, weight and detailed event attributes
- Consecutive error count and a refresh button

## Requirements

Home Assistant **2025.3.0 or newer**, a reachable Kibble server and a pet-bound `state:read` token. Uses local HTTP/HTTPS; no Bluetooth proxy is needed.

## Installation

1. Add `eigger/hass-kibble` as a custom **Integration** repository in HACS.
2. Install the integration and restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration → Kibble**.
4. Enter the Kibble server URL and the pet's `state:read` token.

[Token creation, manual installation and removal](docs/user-guide.md#installation)

## Usage

```yaml
action: button.press
target:
  entity_id: button.bori_refresh_now
```

Use the actual refresh button entity ID created by your installation.

This integration is **read-only**. Failed requests keep the last successful values, so also check the consecutive error count. [Troubleshooting](docs/user-guide.md#limitations-and-troubleshooting)

## Documentation

| Guide | Contents |
|---|---|
| [User guide](docs/user-guide.md) | Setup and tokens, entities/attributes, recorder behavior, troubleshooting, Usage badge meaning |
| [Development and tests](docs/development.md) | Actual HA tests, minimum/current environments, dependencies and commands |
| [Adopted standards](STANDARDS.md) · [Checklist](ADOPTION_CHECKLIST.md) | Common rules and verification records |

## Support and license

Report bugs through [GitHub Issues](https://github.com/eigger/hass-kibble/issues). For questions, usage help and ideas, use [GitHub Discussions](https://github.com/eigger/hass-kibble/discussions). Licensed under [MIT](LICENSE).
