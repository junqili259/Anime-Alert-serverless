from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_currentSeason():
    response = client.get("/")
    assert response.status_code == 200

    
def test_anySeason():
    response = client.get("/season?season=SUMMER&seasonYear=2020")
    assert response.status_code == 200


def test_updateStatus():
    response = client.get("/statusUpdate?id=1")
    assert response.status_code == 200

    response2 = client.get("/statusUpdate?id=2")
    assert response2.json()["errors"][0]["status"] == 404
