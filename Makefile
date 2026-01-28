.PHONY: help dev dev-docker up down build clean docker-clean kill-ports dev-front dev-back dev-lib install-lib deploy-front deploy-back

help:
	@echo "Metro SP MDP - Comandos disponíveis:"
	@echo ""
	@echo "Docker:"
	@echo "  make dev          - Dev com hot reload (Docker)"
	@echo "  make up           - Produção otimizada (Docker)"
	@echo "  make down         - Para Docker"
	@echo "  make build        - Build produção"
	@echo "  make docker-clean - Remove containers parados"
	@echo "  make kill-ports   - Mata processos nas portas 3000 e 8000"
	@echo ""
	@echo "Local (sem Docker):"
	@echo "  make dev-front    - Dev frontend (npm)"
	@echo "  make dev-back     - Dev backend (uvicorn)"
	@echo "  make dev-lib      - Build lib Rust (maturin)"
	@echo "  make install-lib  - Instala lib no backend"
	@echo ""
	@echo "Deploy:"
	@echo "  make deploy-front - Deploy frontend GCP"
	@echo "  make deploy-back  - Deploy backend GCP"
	@echo ""
	@echo "  make clean        - Limpa builds e cache"

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
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload

dev-lib:
	cd packages/metro-mdp-lib && maturin develop --release

install-lib:
	cd backend && pip install -e ../packages/metro-mdp-lib

deploy-front:
	gcloud run deploy frontend --source ./frontend

deploy-back:
	gcloud run deploy backend --source . --dockerfile backend/Dockerfile

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "target" -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/venv frontend/.next packages/*/target
