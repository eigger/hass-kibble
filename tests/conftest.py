"""Small Home Assistant stubs for testing the API client without installing HA."""

import sys
from enum import StrEnum
from types import ModuleType


class _Generic:
    def __class_getitem__(cls, _item):
        return cls


class _ConfigEntry(_Generic):
    pass


class _Platform(StrEnum):
    BUTTON = "button"
    SENSOR = "sensor"


class _Coordinator(_Generic):
    def __init__(self, *args, **kwargs):
        pass


class _Entity(_Generic):
    def __init__(self, coordinator=None, *args, **kwargs):
        self.coordinator = coordinator


class _CoordinatorEntity(_Generic):
    def __init__(self, coordinator=None, *args, **kwargs):
        self.coordinator = coordinator


def _module(name, **attrs):
    module = ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


_module(
    "homeassistant",
    __path__=[],
)
_module("homeassistant.helpers", __path__=[])
_module("homeassistant.components", __path__=[])
_module(
    "homeassistant.config_entries",
    ConfigEntry=_ConfigEntry,
    ConfigFlow=type("ConfigFlow", (), {}),
    ConfigFlowResult=dict,
)
_module("homeassistant.const", Platform=_Platform)
_module(
    "homeassistant.core",
    HomeAssistant=type("HomeAssistant", (), {}),
    callback=lambda f: f,
)
_module(
    "homeassistant.exceptions",
    ConfigEntryAuthFailed=type("ConfigEntryAuthFailed", (Exception,), {}),
)
_module(
    "homeassistant.helpers.aiohttp_client",
    async_get_clientsession=lambda _hass: None,
)
_module(
    "homeassistant.helpers.update_coordinator",
    DataUpdateCoordinator=_Coordinator,
    CoordinatorEntity=_CoordinatorEntity,
    UpdateFailed=type("UpdateFailed", (Exception,), {}),
)
_module("homeassistant.helpers.device_registry", DeviceInfo=dict)
_module(
    "homeassistant.components.sensor",
    SensorEntity=_Entity,
    SensorStateClass=type("SensorStateClass", (), {"MEASUREMENT": "measurement"}),
)
_module("homeassistant.components.button", ButtonEntity=_Entity)
_module("homeassistant.helpers.entity_platform", AddConfigEntryEntitiesCallback=object)
_module("homeassistant.helpers.entity", EntityCategory=type("EntityCategory", (), {}))
