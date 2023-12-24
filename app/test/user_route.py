from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)


def test_user_login():
    # Assuming a user already exists in your test database
    login_data = {
        "username": "existinguser",
        "password": "existingpassword"
    }
    # Make a request to the /users/login endpoint
    response = client.post("/users/login", data=login_data)

    # Check that the login was successful and a token was received
    assert response.status_code == 200
    assert "access_token" in response.json()
