"""
Shared test fixtures.

Strategy:
  - mongomock-motor: in-memory MongoDB compatible with Motor API
  - No real MongoDB needed → tests run anywhere
  - get_db dependency overridden per test
  - mongodb.connect/disconnect patched out (no real connection)
"""
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from database.mongodb import get_db, mongodb
from main import app


@pytest.fixture
async def mock_db():
    """Fresh in-memory MongoDB database for each test."""
    client = AsyncMongoMockClient()
    db = client["test_server_dashboard"]
    yield db
    client.close()


@pytest.fixture
async def client(mock_db):
    """
    HTTPX async test client with:
    - MongoDB lifespan stubbed out (no real connection)
    - get_db dependency overridden to use in-memory mock_db
    """
    app.dependency_overrides[get_db] = lambda: mock_db

    with patch.object(mongodb, "connect", AsyncMock()):
        with patch.object(mongodb, "disconnect", AsyncMock()):
            with patch.object(mongodb, "ping", AsyncMock(return_value=True)):                                                                                                                                                                         
                  async with AsyncClient(                                                                                                                                                                                                               
                      transport=ASGITransport(app=app),
                      base_url="http://test",                                                                                                                                                                                                           
                  ) as ac:
                      yield ac

    app.dependency_overrides.clear()


# ─── Test Data Helpers ────────────────────────────────────────────────────────

SERVER_PAYLOAD = {
    "name": "web-server-01",
    "ip_address": "10.0.0.1",
    "country": "Vietnam",
    "os": "Ubuntu",
    "os_version": "22.04 LTS",
    "platform": "Nginx",
    "arch": "x86_64",
    "status": "Online",
}


def make_server(**overrides) -> dict:
    """Create a valid server payload with optional field overrides."""
    return {**SERVER_PAYLOAD, **overrides}
