import asyncio

import pytest

from tests.conftest import make_server

# Helpers

async def create(client, **overrides) -> dict:
    res = await client.post("/api/v1/servers", json=make_server(**overrides))
    assert res.status_code == 201, res.text
    return res.json()["data"]


# Health

async def test_health_endpoint(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    

# Create
async def test_create_returns_201_with_envelope(client):
    res = await client.post("/api/v1/servers", json=make_server())
    assert res.status_code == 201
    body = res.json()
    assert body["code"] == 200
    assert body["msg"] == "Server created successfully"
    data = body["data"]
    assert data["name"] == "web-server-01"
    assert data["os_version"] == "22.04 LTS"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_create_duplicate_name_returns_409(client):
    await create(client)
    res = await client.post("/api/v1/servers", json=make_server())
    assert res.status_code == 409
    assert res.json()["code"] == 409


async def test_create_invalid_ip_returns_422(client):
    res = await client.post("/api/v1/servers", json=make_server(ip_address="bad-ip"))
    assert res.status_code == 422


async def test_create_missing_required_field_returns_422(client):
    payload = {k: v for k, v in make_server().items() if k != "name"}
    res = await client.post("/api/v1/servers", json=payload)
    assert res.status_code == 422


# Get by ID

async def test_get_server_by_id(client):
    created = await create(client)
    res = await client.get(f"/api/v1/servers/{created['id']}")
    assert res.status_code == 200
    assert res.json()["data"]["id"] == created["id"]


async def test_get_nonexistent_server_returns_404(client):
    res = await client.get("/api/v1/servers/no-such-id")
    assert res.status_code == 404
    assert res.json()["code"] == 404


# List

async def test_list_empty_database(client):
    res = await client.get("/api/v1/servers")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total"] == 0
    assert data["items"] == []
    assert data["page"] == 1
    assert data["total_pages"] == 0


async def test_list_returns_created_server(client):
    await create(client)
    res = await client.get("/api/v1/servers")
    data = res.json()["data"]
    assert data["total"] == 1
    assert len(data["items"]) == 1


async def test_list_pagination(client):
    for i in range(5):
        await create(client, name=f"srv-{i}", ip_address=f"10.0.0.{i+1}")
    res = await client.get("/api/v1/servers?page=1&size=3")
    data = res.json()["data"]
    assert data["total"] == 5
    assert len(data["items"]) == 3
    assert data["total_pages"] == 2


async def test_list_filter_by_status(client):
    await create(client, name="online-srv", ip_address="10.0.0.1", status="Online")
    await create(client, name="offline-srv", ip_address="10.0.0.2", status="Offline")
    res = await client.get("/api/v1/servers?status=Online")
    data = res.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["name"] == "online-srv"


async def test_list_search_by_name(client):
    await create(client, name="web-server", ip_address="10.0.0.1")
    await create(client, name="db-server", ip_address="10.0.0.2")
    res = await client.get("/api/v1/servers?name=web")
    data = res.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["name"] == "web-server"


# Update

async def test_update_server_fields(client):
    created = await create(client)
    res = await client.put(
        f"/api/v1/servers/{created['id']}",
        json={"status": "Offline", "platform": "Apache"},
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["status"] == "Offline"
    assert data["platform"] == "Apache"
    assert data["name"] == "web-server-01"  # unchanged


async def test_update_rename_server(client):
    created = await create(client)
    res = await client.put(
        f"/api/v1/servers/{created['id']}",
        json={"name": "renamed-server"},
    )
    assert res.status_code == 200
    assert res.json()["data"]["name"] == "renamed-server"


async def test_update_rename_to_existing_name_returns_409(client):
    srv1 = await create(client, name="first", ip_address="10.0.0.1")
    await create(client, name="second", ip_address="10.0.0.2")
    res = await client.put(f"/api/v1/servers/{srv1['id']}", json={"name": "second"})
    assert res.status_code == 409


async def test_update_nonexistent_returns_404(client):
    res = await client.put("/api/v1/servers/no-such-id", json={"status": "Offline"})
    assert res.status_code == 404


# Delete

async def test_delete_server(client):
    created = await create(client)
    res = await client.delete(f"/api/v1/servers/{created['id']}")
    assert res.status_code == 200
    # Verify deleted
    get_res = await client.get(f"/api/v1/servers/{created['id']}")
    assert get_res.status_code == 404


async def test_delete_nonexistent_returns_404(client):
    res = await client.delete("/api/v1/servers/no-such-id")
    assert res.status_code == 404


# ReDoS / regex injection

async def test_search_regex_special_chars_treated_as_literal(client):
    await create(client, name="web.server", ip_address="10.0.0.1")
    await create(client, name="web-server", ip_address="10.0.0.2")

    res = await client.get("/api/v1/servers?name=web.server")
    data = res.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["name"] == "web.server"


async def test_search_malicious_regex_pattern_does_not_crash(client):
    await create(client, name="safe-server", ip_address="10.0.0.1")

    res = await client.get("/api/v1/servers?name=(a%2B)%2B")
    assert res.status_code == 200
    assert res.json()["data"]["total"] == 0


async def test_search_brackets_treated_as_literal(client):
    await create(client, name="[Oo]nline-server", ip_address="10.0.0.1")
    await create(client, name="Online-server", ip_address="10.0.0.2")

    res = await client.get("/api/v1/servers?name=%5BOo%5Dnline")
    data = res.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["name"] == "[Oo]nline-server"


# Race condition

async def test_concurrent_create_same_name_returns_409_not_500(client):
    results = await asyncio.gather(
        client.post("/api/v1/servers", json=make_server()),
        client.post("/api/v1/servers", json=make_server()),
        return_exceptions=True,
    )
    statuses = sorted([r.status_code for r in results])
    assert statuses == [201, 409], f"Expected [201, 409], got {statuses}"
