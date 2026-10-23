<!-- hass-standards:header:start -->
# Kibble Home Assistant Integration (hass-kibble)

A read-only Home Assistant custom integration for Kibble pet care records.

**English** | [한국어](README.ko.md)

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat)](https://github.com/eigger/hass-kibble/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat)](#installation)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.3.0-41BDF5?style=flat)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat&label=Tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/validate.yml?branch=master&style=flat&label=Validate)](https://github.com/eigger/hass-kibble/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/eigger/hass-kibble/total?style=flat&color=41BDF5&label=Downloads)](https://github.com/eigger/hass-kibble/releases)
<!-- hass-standards:badges:end -->
<!-- hass-standards:header:end -->

![Kibble](custom_components/kibble/brand/logo.png)

A **read-only** custom Home Assistant integration for Kibble. It polls the daily summary, individual feeding and care records, overdue medication and reminders every five minutes and exposes them as sensors.

## Features

- Sensors for daily feeding and care records, overdue medication and reminders
- Daily totals, weight and detailed event attributes
- Consecutive error count and a refresh button

## Requirements

Home Assistant **2025.3.0 or newer**, a reachable Kibble server and a pet-bound `state:read` token. Uses local HTTP/HTTPS; no Bluetooth proxy is needed.

## Installation

<!-- hass-standards:installation:start -->
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=eigger&repository=hass-kibble&category=integration)
<!-- hass-standards:installation:end -->

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
| [User guide](docs/user-guide.md) | Setup and tokens, entities/attributes, recorder behavior, troubleshooting, Downloads badge meaning |
| [Development and tests](docs/development.md) | Actual HA tests, minimum/current environments, dependencies and commands |
| [Adopted standards](STANDARDS.md) · [Checklist](ADOPTION_CHECKLIST.md) | Common rules and verification records |

<!-- hass-standards:support:start -->
## Support

- [Issues](https://github.com/eigger/hass-kibble/issues): Report bugs or request features.
- [Discussions](https://github.com/eigger/hass-kibble/discussions): Ask questions and share your experience.
<!-- hass-standards:support:end -->

<!-- hass-standards:related-projects:start -->
## Related Projects

- [Kibble](https://github.com/eigger/kibble): The pet care server used by this integration and the source of its brand icon.
<!-- hass-standards:related-projects:end -->

<!-- hass-standards:license:start -->
## License

Released under the [MIT License](LICENSE).
<!-- hass-standards:license:end -->
