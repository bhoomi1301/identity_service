from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_primary_contact():
    response = client.post("/identify", json={"email": "unit@test.com", "phoneNumber": "1231231234"})
    assert response.status_code == 200
    data = response.json()
    assert data["primaryContactId"] > 0
    assert "unit@test.com" in data["emails"]
    assert "1231231234" in data["phoneNumbers"]

def test_create_secondary_contact():
    response = client.post("/identify", json={"email": "unit@test.com", "phoneNumber": "0009991111"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["secondaryContactIds"]) >= 1
