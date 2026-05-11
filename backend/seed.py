import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from motor.motor_asyncio import AsyncIOMotorClient

from core.conf import settings


SERVERS = [
    {"name": "web-hanoi-01", "ip_address": "103.56.76.10", "country": "Vietnam", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "Nginx", "arch": "x86_64", "status": "Online"},
    {"name": "web-hanoi-02", "ip_address": "103.56.76.11", "country": "Vietnam", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "Nginx", "arch": "x86_64", "status": "Online"},
    {"name": "db-hcm-01", "ip_address": "103.90.224.50", "country": "Vietnam", "os": "Debian", "os_version": "12 Bookworm", "platform": "MongoDB", "arch": "x86_64", "status": "Online"},
    {"name": "api-hcm-01", "ip_address": "103.90.224.51", "country": "Vietnam", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "FastAPI", "arch": "x86_64", "status": "Offline"},
    {"name": "sg-web-01", "ip_address": "18.138.71.120", "country": "Singapore", "os": "Ubuntu", "os_version": "24.04 LTS", "platform": "Nginx", "arch": "x86_64", "status": "Online"},
    {"name": "sg-cache-01", "ip_address": "18.138.71.121", "country": "Singapore", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "Redis", "arch": "x86_64", "status": "Online"},
    {"name": "sg-db-01", "ip_address": "18.138.71.130", "country": "Singapore", "os": "CentOS", "os_version": "9 Stream", "platform": "PostgreSQL", "arch": "x86_64", "status": "Online"},
    {"name": "us-east-web-01", "ip_address": "54.82.14.230", "country": "United States", "os": "Amazon Linux", "os_version": "2023", "platform": "Apache", "arch": "x86_64", "status": "Online"},
    {"name": "us-east-api-01", "ip_address": "54.82.14.231", "country": "United States", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "FastAPI", "arch": "ARM64", "status": "Online"},
    {"name": "us-west-cdn-01", "ip_address": "52.52.100.5", "country": "United States", "os": "Alpine Linux", "os_version": "3.19", "platform": "Nginx", "arch": "x86_64", "status": "Offline"},
    {"name": "de-fra-01", "ip_address": "138.201.44.100", "country": "Germany", "os": "Debian", "os_version": "12 Bookworm", "platform": "Docker", "arch": "x86_64", "status": "Online"},
    {"name": "de-fra-02", "ip_address": "138.201.44.101", "country": "Germany", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "Kubernetes", "arch": "x86_64", "status": "Online"},
    {"name": "jp-tokyo-01", "ip_address": "13.115.43.220", "country": "Japan", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "Nginx", "arch": "x86_64", "status": "Online"},
    {"name": "jp-tokyo-02", "ip_address": "13.115.43.221", "country": "Japan", "os": "CentOS", "os_version": "9 Stream", "platform": "Apache", "arch": "x86_64", "status": "Offline"},
    {"name": "uk-lon-01", "ip_address": "18.169.123.45", "country": "United Kingdom", "os": "Ubuntu", "os_version": "24.04 LTS", "platform": "Nginx", "arch": "ARM64", "status": "Online"},
    {"name": "kr-seoul-01", "ip_address": "52.78.230.10", "country": "South Korea", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "FastAPI", "arch": "x86_64", "status": "Online"},
    {"name": "au-sydney-01", "ip_address": "13.239.88.30", "country": "Australia", "os": "Ubuntu", "os_version": "22.04 LTS", "platform": "Nginx", "arch": "x86_64", "status": "Online"},
    {"name": "nl-ams-01", "ip_address": "82.196.13.100", "country": "Netherlands", "os": "Debian", "os_version": "12 Bookworm", "platform": "Nginx", "arch": "x86_64", "status": "Online"},
]


async def seed() -> None:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]

    # Clear existing data
    await db["servers"].delete_many({})
    await db["activities"].delete_many({})
    print("Cleared existing data")

    # Insert servers with staggered created_at dates
    base_time = datetime.now(timezone.utc) - timedelta(days=30)
    for i, srv in enumerate(SERVERS):
        now = base_time + timedelta(days=i * 1.5, hours=i * 3)
        doc = {
            "_id": str(uuid.uuid4()),
            **srv,
            "created_at": now,
            "updated_at": now,
        }
        await db["servers"].insert_one(doc)
        await db["activities"].insert_one({
            "_id": str(uuid.uuid4()),
            "server_id": doc["_id"],
            "server_name": doc["name"],
            "action": "created",
            "detail": f"Server '{doc['name']}' was created",
            "timestamp": now,
        })

    print(f"Seeded {len(SERVERS)} servers and {len(SERVERS)} activity entries")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
