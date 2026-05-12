from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from middleware.rate_limit import RateLimitMiddleware


def make_mock_settings(
    enabled: bool = True,
    read_limit: int = 3,
    write_limit: int = 2,
) -> MagicMock:

    mock = MagicMock()
    mock.RATE_LIMIT_ENABLED = enabled
    mock.RATE_LIMIT_PER_MINUTE = read_limit
    mock.RATE_LIMIT_WRITE_PER_MINUTE = write_limit
    return mock


@pytest.fixture
def make_client(monkeypatch):

    async def _factory(
        enabled: bool = True,
        read_limit: int = 3,
        write_limit: int = 2,
    ):
        mock_cfg = make_mock_settings(enabled, read_limit, write_limit)

        monkeypatch.setattr(
            "middleware.rate_limit.settings",
            mock_cfg,
        )

        app = FastAPI()
        app.add_middleware(RateLimitMiddleware)

        @app.get("/read")
        async def read_endpoint():
            return {"ok": True}

        @app.post("/write")
        async def write_endpoint():
            return {"ok": True}

        return AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        )

    return _factory


# Read limit tests


async def test_read_requests_within_limit_pass(make_client):

    async with await make_client(read_limit=3) as client:
        for i in range(3):
            res = await client.get("/read")

            assert (
                res.status_code == 200
            ), f"Request {i + 1} was unexpectedly blocked"


async def test_read_requests_exceeding_limit_return_429(make_client):

    async with await make_client(read_limit=3) as client:
        for _ in range(3):
            await client.get("/read")

        res = await client.get("/read")

        assert res.status_code == 429


async def test_429_response_has_correct_envelope(make_client):

    async with await make_client(read_limit=1) as client:
        await client.get("/read")

        res = await client.get("/read")

    assert res.status_code == 429

    body = res.json()

    assert body["code"] == 429
    assert "Too many requests" in body["msg"]
    assert "data" in body


async def test_429_response_includes_retry_after_header(make_client):

    async with await make_client(read_limit=1) as client:
        await client.get("/read")

        res = await client.get("/read")

    assert "retry-after" in res.headers
    assert res.headers["retry-after"] == "60"


# Write limit tests


async def test_write_requests_have_stricter_limit(make_client):

    async with await make_client(
        read_limit=10,
        write_limit=2,
    ) as client:
        for _ in range(2):
            res = await client.post("/write")

            assert res.status_code == 200

        res = await client.post("/write")

        assert res.status_code == 429


async def test_read_and_write_limits_are_independent(make_client):

    async with await make_client(
        read_limit=2,
        write_limit=2,
    ) as client:
        for _ in range(2):
            await client.get("/read")

        res = await client.get("/read")

        assert res.status_code == 429, (
            "Read requests should be rate-limited"
        )

        res = await client.post("/write")

        assert res.status_code == 200, (
            "Write requests should not be affected "
            "by read limits"
        )


async def test_disabled_rate_limit_allows_all_requests(make_client):

    async with await make_client(
        enabled=False,
        read_limit=2,
    ) as client:
        for i in range(5):
            res = await client.get("/read")

            assert (
                res.status_code == 200
            ), f"Request {i + 1} was blocked unexpectedly"


async def test_rate_limit_is_per_ip(make_client):

    app = FastAPI()
    app.add_middleware(RateLimitMiddleware)

    @app.get("/ping")
    async def ping():
        return {"ok": True}

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        res = await client.get("/ping")

        assert res.status_code == 200