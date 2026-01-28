.PHONY: help dev up down build build-dev clean docker-clean kill-ports dev-front dev-back

help:
	@echo "Metro SP MDP - Available commands:"
	@echo ""
	@echo "Docker:"
	@echo "  make dev          - Dev with hot reload (Docker)"
	@echo "  make up           - Production build (Docker)"
	@echo "  make down         - Stop Docker containers"
	@echo "  make build        - Build production frontend"
	@echo "  make build-dev    - Build dev containers"
	@echo "  make docker-clean - Remove stopped containers"
	@echo "  make kill-ports   - Kill processes on ports 3000 and 8000"
	@echo ""
	@echo "Local (without Docker):"
	@echo "  make dev-front    - Dev frontend (npm)"
	@echo "  make dev-back     - Dev backend (uvicorn)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Clean builds and cache"

dev:
	@docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true
	docker-compose -f docker-compose.dev.yml up --build

up:
	docker-compose up

down:
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

build:
	docker-compose build frontend

build-dev:
	docker-compose -f docker-compose.dev.yml build

docker-clean:
	docker-compose down -v --remove-orphans
	docker container prune -f
	docker network prune -f

kill-ports:
	@echo "Matando processos nas portas 3000 e 8000..."
	@lsof -ti:3000 | xargs kill -9 2>/dev/null || true
	@lsof -ti:8000 | xargs kill -9 2>/dev/null || true
	@echo "Portas liberadas!"

dev-front:
	cd frontend && npm run dev

dev-back:
	cd backend && uv run uvicorn app.main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "target" -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.venv frontend/.next packages/*/target
