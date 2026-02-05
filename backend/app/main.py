import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from metro_mdp import fuzz_string, solve_route
from pydantic import BaseModel, Field

stations_df = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global stations_df
    data_path = Path(__file__).parent.parent / "data" / "stations.csv"
    stations_df = pd.read_csv(data_path)
    yield


# Disable docs in production
is_production = os.getenv("ENVIRONMENT") == "production"

app = FastAPI(
    title="Metro SP MDP API",
    description="API for Markov Decision Process modeling of São Paulo metro system",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
)

# CORS configuration - restrict to frontend domain
allowed_origins = [
    "https://metro-sp-mdp-shippuden.vercel.app",
    "http://localhost:3000",  # For local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD"],
    allow_headers=["*"],
)


@app.get("/")
@app.head("/")
async def root():
    return {
        "message": "Metro SP MDP API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
@app.head("/health")
async def health_check():
    return {"status": "healthy"}


class RouteRequest(BaseModel):
    start: str = Field(..., max_length=100, description="Starting station")
    end: str = Field(..., max_length=100, description="Destination station")


class RouteResponse(BaseModel):
    path: list[str]


@app.post("/api/route", response_model=RouteResponse)
async def find_route(route_request: RouteRequest):
    start_station = fuzz_string(route_request.start.lower().strip(), stations_df["station"])
    end_station = fuzz_string(route_request.end.lower().strip(), stations_df["station"])

    # TODO: adicionar cache pra rotas mais comuns (luz-paulista, se-luz, etc)
    try:
        # Add timeout to prevent long-running requests
        path = await asyncio.wait_for(
            asyncio.to_thread(solve_route, stations_df, start_station, end_station),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail="Route calculation timed out. Please try again."
        )

    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"No route found from {route_request.start} to {route_request.end}"
        )

    return RouteResponse(path=path)


@app.get("/api/stations")
async def get_stations():
    stations = stations_df[["station", "name", "line", "lat", "lon"]].to_dict(orient="records")
    return {"stations": stations, "count": len(stations)}
