import pytest

@pytest.mark.asyncio
async def test_bot_user_agent_allowed(client):
    await client.post(
        "/admin/create",
        params={"long_url": "https://example.com", "custom_code": "bot"},
        headers={"x-api-key": "test-admin-token"},
    )

    res = await client.get(
        "/r/bot",
        headers={"user-agent": "googlebot"},
        follow_redirects=False,
    )

    assert res.status_code in (301, 302)
