# Metro SP MDP Shippuden

Markov Decision Process applied to São Paulo Metro System for optimal route planning.

## Quick Start

```bash
# Local development
docker-compose up

# Build backend (root context)
docker build -f backend/Dockerfile -t metro-backend .

# Build frontend
docker build -f frontend/Dockerfile -t metro-frontend ./frontend

# Deploy to GCP Cloud Run
gcloud run deploy backend --source . --dockerfile backend/Dockerfile
gcloud run deploy frontend --source ./frontend
```

## URLs

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

## Data

Frontend dynamically loads stations from `/public/data/metrosp_stations.csv` using papaparse.
