from unittest.mock import AsyncMock, patch

from app.server.crud.crud_server import server_dao
from tests.conftest import make_server


async def _post_server(client, name, ip, os="Ubuntu", platform="Nginx") -> None:
    await client.post("/api/v1/servers", json=make_server(name=name, ip_address=ip, os=os, platform=platform))


# /stats/overview 

async def test_overview_empty_database(client):
    with patch.object(server_dao, "count_by_field", AsyncMock(return_value=[])):
        res = await client.get("/api/v1/stats/overview")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_servers"] == 0
    assert data["by_os"] == []


async def test_overview_counts_total_servers(client):
    await _post_server(client, "s1", "10.0.0.1")
    await _post_server(client, "s2", "10.0.0.2")
    mock_agg = AsyncMock(side_effect=[
        [{"_id": "Ubuntu", "count": 2}],
        [{"_id": "Nginx", "count": 2}],
        [{"_id": "x86_64", "count": 2}],
        [{"_id": "Online", "count": 2}],
    ])
    with patch.object(server_dao, "count_by_field", mock_agg):
        res = await client.get("/api/v1/stats/overview")
    data = res.json()["data"]
    assert data["total_servers"] == 2
    assert data["by_os"] == [{"name": "Ubuntu", "count": 2}]


# /stats/timeseries

async def test_timeseries_default_7d_range(client):
    mock_ts = [{"date": "2024-03-01", "count": 2}]
    with patch.object(server_dao, "get_timeseries", AsyncMock(return_value=mock_ts)):
        res = await client.get("/api/v1/stats/timeseries")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["range"] == "7d"
    assert data["timeseries"] == mock_ts
    assert "start" in data
    assert "end" in data
    assert "new_in_range" in data


async def test_timeseries_24h_uses_hour_grouping(client):
    with patch.object(server_dao, "get_timeseries", AsyncMock(return_value=[])) as mock:
        await client.get("/api/v1/stats/timeseries?range=24h")
    _, kwargs = mock.call_args
    assert kwargs.get("group_by") == "hour"


async def test_timeseries_7d_uses_day_grouping(client):
    with patch.object(server_dao, "get_timeseries", AsyncMock(return_value=[])) as mock:
        await client.get("/api/v1/stats/timeseries?range=7d")
    _, kwargs = mock.call_args
    assert kwargs.get("group_by") == "day"


async def test_timeseries_custom_missing_dates_returns_400(client):
    res = await client.get("/api/v1/stats/timeseries?range=custom")
    assert res.status_code == 400
    assert res.json()["code"] == 400


async def test_timeseries_custom_invalid_date_format_returns_400(client):
    res = await client.get(
        "/api/v1/stats/timeseries?range=custom&start=not-a-date&end=also-bad"
    )
    assert res.status_code == 400


async def test_timeseries_custom_valid_range(client):
    mock_ts = [{"date": "2024-01-15", "count": 1}]
    with patch.object(server_dao, "get_timeseries", AsyncMock(return_value=mock_ts)):
        res = await client.get(
            "/api/v1/stats/timeseries?range=custom&start=2024-01-01&end=2024-01-31"
        )
    assert res.status_code == 200
    assert res.json()["data"]["range"] == "custom"
