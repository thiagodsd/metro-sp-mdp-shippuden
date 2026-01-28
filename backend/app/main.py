from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Metro SP MDP API",
    description="API for Markov Decision Process modeling of São Paulo metro system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    """Find optimal route between two stations using MDP."""
    # TODO: Implement MDP algorithm
    # For now, returns a hardcoded valid path from Butantã to Luz
    dummy_path = [
        "butanta",
        "pinheiros",
        "faria-lima",
        "fradique-coutinho",
        "oscar-freire",
        "paulista",
        "republica",
        "luz",
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
