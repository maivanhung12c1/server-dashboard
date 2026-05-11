.PHONY: dev dev-d dev-build down down-v restart-be logs-be logs-mongo shell-be shell-mongo lint lint-fix test-unit test-integration test

# Development

dev:
	docker compose -f docker-compose.dev.yml up --remove-orphans

dev-d:
	docker compose -f docker-compose.dev.yml up -d --remove-orphans

dev-build:
	docker compose -f docker-compose.dev.yml up --build -d --remove-orphans

down:
	docker compose -f docker-compose.dev.yml down

down-v:
	docker compose -f docker-compose.dev.yml down -v

restart-be:
	docker compose -f docker-compose.dev.yml restart backend

# Logs

logs-be:
	docker compose -f docker-compose.dev.yml logs -f backend

logs-mongo:
	docker compose -f docker-compose.dev.yml logs -f mongodb

# Shell

shell-be:
	docker compose -f docker-compose.dev.yml exec backend bash

shell-mongo:
	docker compose -f docker-compose.dev.yml exec mongodb mongosh \
	  -u $${MONGO_USER:-admin} -p $${MONGO_PASSWORD:-changeme} \
	  --authenticationDatabase admin $${MONGO_DB:-server_dashboard}

# Lint

lint:
	docker compose -f docker-compose.dev.yml exec backend ruff check .

lint-fix:
	docker compose -f docker-compose.dev.yml exec backend ruff check . --fix

# Tests

test-unit:
	docker compose -f docker-compose.dev.yml exec backend \
	  pytest tests/unit/ -v

test-integration:
	docker compose -f docker-compose.dev.yml exec backend \
	  pytest tests/integration/ -v

test:
	docker compose -f docker-compose.dev.yml exec backend \
	  pytest tests/ -v --tb=short