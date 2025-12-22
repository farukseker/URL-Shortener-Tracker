import pytest

@pytest.mark.asyncio
async def test_admin_create_short(client):
    res = await client.post(
        "/admin/create",
        params={"long_url": "https://example.com", "custom_code": "example"},
        headers={"x-api-key": "test-admin-token"},
    )

    assert res.status_code == 200
    assert res.json()["short"] == "/r/example"

@pytest.mark.asyncio
async def test_admin_create_unauthorized(client):
    res = await client.post(
        "/admin/create",
        params={"long_url": "https://example.com"},
    )

    assert res.status_code == 404
