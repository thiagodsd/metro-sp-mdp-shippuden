from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from metro_mdp import fuzz_string, solve_route
from pydantic import BaseModel

app = FastAPI(
    title="Metro SP MDP API",
    description="API for Markov Decision Process modeling of São Paulo metro system",
    version="0.1.0",
)

# Load station data at startup
DATA_PATH = Path(__file__).parent.parent / "data" / "stations.csv"
stations_df = pd.read_csv(DATA_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def clean_station_name(name: str) -> str:
    """Remove noise words from station names for better fuzzy matching."""
    name = name.lower().strip()
    noise_words = ["estação", "estacao", "station", "da", "de", "do"]
    for word in noise_words:
        name = name.replace(word, "")
    return name.strip()


@app.get("/")
async def root():
    return {
        "message": "Metro SP MDP API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


class RouteRequest(BaseModel):
    start: str
    end: str


class RouteResponse(BaseModel):
    path: list[str]
    distance: float | None = None
    time: float | None = None


@app.post("/api/route", response_model=RouteResponse)
async def find_route(request: RouteRequest):
    """Find optimal route between two stations using MDP."""
    try:
        # Clean and fuzzy match station names
        start_cleaned = clean_station_name(request.start)
        end_cleaned = clean_station_name(request.end)

        start_station = fuzz_string(start_cleaned, stations_df["station"])
        end_station = fuzz_string(end_cleaned, stations_df["station"])

        # Find route using MDP
        path = solve_route(stations_df, start_station, end_station)

        if not path:
            raise HTTPException(
                status_code=404, detail=f"No route found from {request.start} to {request.end}"
            )

        return RouteResponse(path=path, distance=None, time=None)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding route: {str(e)}")


@app.get("/api/stations")
async def get_stations():
    """Get all metro stations."""
    stations = stations_df[["station", "name", "line", "lat", "lon"]].to_dict(orient="records")
    return {"stations": stations, "count": len(stations)}
