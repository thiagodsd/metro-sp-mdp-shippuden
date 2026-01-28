from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


# Example endpoint - replace with your actual MDP logic
@app.get("/api/stations")
async def get_stations():
    return {
        "stations": [
            {"id": 1, "name": "Sé", "line": "blue"},
            {"id": 2, "name": "República", "line": "red"},
        ]
    }
