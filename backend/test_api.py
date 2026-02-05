import asyncio
from app.main import app

# Simular request
async def test():
    try:
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.post("/api/route", json={"start": "se", "end": "luz"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
