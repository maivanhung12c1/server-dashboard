from unittest.mock import AsyncMock, patch

from database.mongodb import mongodb


async def test_health_returns_200_when_db_connected(client):
    res = await client.get("/health")

    assert res.status_code == 200

    body = res.json()

    assert body["status"] == "ok"
    assert "version" in body


async def test_health_returns_503_when_db_unreachable(client):
    with patch.object(
        mongodb,
        "ping",
        AsyncMock(return_value=False),
    ):
        res = await client.get("/health")

    assert res.status_code == 503

    body = res.json()

    assert body["status"] == "degraded"
    assert body["db"] == "unreachable"
    assert "version" in body


async def test_health_503_does_not_expose_internal_error_detail(client):
    with patch.object(
        mongodb,
        "ping",
        AsyncMock(return_value=False),
    ):
        res = await client.get("/health")

    body = res.json()

    assert "traceback" not in str(body).lower()
    assert "exception" not in str(body).lower()