from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Metro SP MDP API",
    description="API for Markov Decision Process modeling of São Paulo metro system",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    """
    Find optimal route between two stations using MDP.

    For now returns a dummy path. Will be replaced with actual MDP implementation.
    """
    # TODO: Implement actual MDP algorithm
    # This is a placeholder that returns a simple path
    dummy_path = [
        request.start,
        "republica",
        "luz",
        request.end,
    ]

    return RouteResponse(
        path=dummy_path,
        distance=None,
        time=None,
    )


@app.get("/api/stations")
async def get_stations():
    """Get all metro stations."""
    return {
        "stations": [
            {"id": 1, "name": "Sé", "line": "blue"},
            {"id": 2, "name": "República", "line": "red"},
        ]
    }
