from unittest.mock import AsyncMock

from database.mongodb import mongodb


async def test_ping_returns_false_when_client_is_none():
    original_client = mongodb.client

    try:
        mongodb.client = None

        result = await mongodb.ping()

        assert result is False
    finally:
        mongodb.client = original_client


async def test_ping_returns_false_when_command_raises():
    mock_client = AsyncMock()
    mock_client.admin.command.side_effect = Exception(
        "connection reset by peer"
    )

    original_client = mongodb.client

    try:
        mongodb.client = mock_client

        result = await mongodb.ping()

        assert result is False
    finally:
        mongodb.client = original_client


async def test_ping_returns_true_when_command_succeeds():
    mock_client = AsyncMock()
    mock_client.admin.command.return_value = {"ok": 1}

    original_client = mongodb.client

    try:
        mongodb.client = mock_client

        result = await mongodb.ping()

        assert result is True
    finally:
        mongodb.client = original_client