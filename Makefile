.PHONY: dev dev-d down down-v restart-be logs-be logs-mongo shell-be shell-mongo

# Development

dev:
	docker compose -f docker-compose.dev.yml up

dev-d:
	docker compose -f docker-compose.dev.yml up -d

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