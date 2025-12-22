import pytest

@pytest.mark.asyncio
async def test_redirect(client):
    await client.post(
        "/admin/create",
        params={"long_url": "https://example.com", "custom_code": "redir"},
        headers={"x-api-key": "test-admin-token"},
    )

    res = await client.get("/r/redir", follow_redirects=False)

    assert res.status_code in (301, 302)
    assert res.headers["location"] == "https://example.com"
