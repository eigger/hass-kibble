"""Exercise config and reauth flows through the actual HA flow manager."""

import pytest
from homeassistant import config_entries, data_entry_flow


async def test_create_entry_and_duplicate(hass, api_response):
    result = await hass.config_entries.flow.async_init(
        "kibble", context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is data_entry_flow.FlowResultType.FORM
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"url": " http://kibble.test/ ", "api_token": " test-token "}
    )
    await hass.async_block_till_done()
    assert result["type"] is data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["data"] == {"url": "http://kibble.test", "api_token": "test-token"}
    assert result["result"].unique_id == "pet-1"
    duplicate = await hass.config_entries.flow.async_init(
        "kibble",
        context={"source": config_entries.SOURCE_USER},
        data={"url": "http://kibble.test", "api_token": "test-token"},
    )
    assert duplicate["type"] is data_entry_flow.FlowResultType.ABORT
    assert duplicate["reason"] == "already_configured"


@pytest.mark.parametrize(
    ("status", "expected"),
    [(401, "invalid_auth"), (403, "invalid_auth"), (500, "cannot_connect")],
)
async def test_connection_errors(hass, aioclient_mock, status, expected):
    aioclient_mock.get("http://kibble.test/api/states", status=status)
    result = await hass.config_entries.flow.async_init(
        "kibble",
        context={"source": config_entries.SOURCE_USER},
        data={"url": "http://kibble.test", "api_token": "test-token"},
    )
    assert result["type"] is data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"base": expected}


async def test_invalid_url(hass):
    result = await hass.config_entries.flow.async_init(
        "kibble",
        context={"source": config_entries.SOURCE_USER},
        data={"url": "ftp://kibble.test", "api_token": "test-token"},
    )
    assert result["errors"] == {"base": "unknown"}


async def test_reauth_errors_wrong_pet_and_success(
    hass, entry, aioclient_mock, state_payload
):
    result = await hass.config_entries.flow.async_init(
        "kibble",
        context={"source": config_entries.SOURCE_REAUTH, "entry_id": entry.entry_id},
        data=entry.data,
    )
    assert result["step_id"] == "reauth_confirm"
    for status, error in [(401, "invalid_auth"), (500, "cannot_connect")]:
        aioclient_mock.clear_requests()
        aioclient_mock.get("http://kibble.test/api/states", status=status)
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {"api_token": "new-token"}
        )
        assert result["errors"] == {"base": error}
    aioclient_mock.clear_requests()
    state_payload["pet"]["id"] = "another-pet"
    aioclient_mock.get("http://kibble.test/api/states", json=state_payload)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"api_token": "new-token"}
    )
    assert result["errors"] == {"base": "wrong_pet"}
    aioclient_mock.clear_requests()
    state_payload["pet"]["id"] = "pet-1"
    aioclient_mock.get("http://kibble.test/api/states", json=state_payload)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"api_token": " new-token "}
    )
    await hass.async_block_till_done()
    assert result["type"] is data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert entry.data["api_token"] == "new-token"
