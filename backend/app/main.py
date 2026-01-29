from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from metro_mdp import fuzz_string, solve_route
from pydantic import BaseModel

stations_df = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global stations_df
    data_path = Path(__file__).parent.parent / "data" / "stations.csv"
    stations_df = pd.read_csv(data_path)
    yield


app = FastAPI(
    title="Metro SP MDP API",
    description="API for Markov Decision Process modeling of São Paulo metro system",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
    start: str
    end: str


class RouteResponse(BaseModel):
    path: list[str]


@app.post("/api/route", response_model=RouteResponse)
async def find_route(request: RouteRequest):
    start_station = fuzz_string(request.start.lower().strip(), stations_df["station"])
    end_station = fuzz_string(request.end.lower().strip(), stations_df["station"])

    path = solve_route(stations_df, start_station, end_station)

    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"No route found from {request.start} to {request.end}"
        )

    return RouteResponse(path=path)


@app.get("/api/stations")
async def get_stations():
    stations = stations_df[["station", "name", "line", "lat", "lon"]].to_dict(orient="records")
    return {"stations": stations, "count": len(stations)}
