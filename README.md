# Server Dashboard

A production-grade fullstack server monitoring dashboard built with FastAPI, MongoDB, React, and Docker.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI 0.115 + Motor (async MongoDB) |
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Database | MongoDB 7 |
| Proxy | Nginx |
| Container | Docker + Docker Compose |

## Quick Start (Development)

```bash
# 1. Copy and configure environment
cp .env.example .env
# Edit .env with your values

# 2. Start all services
docker compose -f docker-compose.dev.yml up

# 3. Seed sample data
docker compose -f docker-compose.dev.yml exec backend python seed.py

# 4. Access
#   Frontend: http://localhost:3000
#   Backend API: http://localhost:8000
#   Swagger Docs: http://localhost:8000/docs
#   MongoDB: localhost:27017
```

## Project Structure

```
my-server-dashboard/
├── backend/          FastAPI application
├── frontend/         React + Vite application
├── nginx/           Nginx configs
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .env.example
└── Makefile
```

## Development Commands

```bash
make dev          # Start dev environment
make down         # Stop all containers
make logs-be      # Backend logs
make seed         # Seed sample data
make test         # Run backend tests
make shell-be     # Shell into backend container
make shell-mongo  # MongoDB shell
```