#!/bin/bash
set -e

echo "Pre-CD Check - Validating changes locally..."
echo ""

FRONTEND_CHANGED=false
BACKEND_CHANGED=false

# Check what changed
if git diff --name-only HEAD | grep -q "^frontend/"; then
    FRONTEND_CHANGED=true
fi

if git diff --name-only HEAD | grep -q "^backend/"; then
    BACKEND_CHANGED=true
fi

# If no git changes detected, check everything
if [ "$FRONTEND_CHANGED" = false ] && [ "$BACKEND_CHANGED" = false ]; then
    echo "WARNING: No git changes detected, checking all components..."
    FRONTEND_CHANGED=true
    BACKEND_CHANGED=true
fi

# Frontend checks
if [ "$FRONTEND_CHANGED" = true ]; then
    echo "→ Frontend checks"
    cd frontend

    echo "  - Installing dependencies..."
    npm ci --silent

    echo "  - Running lint..."
    npm run lint

    echo "  - Type checking..."
    npx tsc --noEmit

    echo "  - Building..."
    npm run build

    cd ..
    echo "  [OK] Frontend passed"
    echo ""
fi

# Backend checks
if [ "$BACKEND_CHANGED" = true ]; then
    echo "→ Backend checks"
    cd backend

    echo "  - Syncing dependencies (including dev)..."
    uv sync --all-extras --quiet

    echo "  - Running lint..."
    uv run ruff check .

    echo "  - Checking format..."
    uv run ruff format --check .

    cd ..
    echo "  [OK] Backend passed"
    echo ""
fi

echo "[OK] All checks passed! Safe to push."
