import uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient
from Backend.endpoints.auth_login import router as login_router
from Backend.endpoints.auth_register import router as register_router

# -------- FastAPI Test App --------
app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)

client = TestClient(app)

# -------- Helpers --------
def random_username():
    return f"user_{uuid.uuid4().hex[:8]}"

# -------- Integration Tests --------

# tests if a new user can register successfully
def test_register_success():
    username = random_username()

    response = client.post("/register", json={
        "username": username,
        "password": "testpass",
        "birthdate": "1999-01-01",
        "business_type": "Self-employed",
        "business_field": "Food",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"

# tests if registering an existing user fails
def test_register_existing_user():
    username = random_username()

    client.post("/register", json={
        "username": username,
        "password": "pass1234",
        "birthdate": "1990-01-01",
        "business_type": "Self-employed",
        "business_field": "Food",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    response = client.post("/register", json={
        "username": username,
        "password": "pass1234",
        "birthdate": "1990-01-01",
        "business_type": "Self-employed",
        "business_field": "Food",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

# tests if registering with missing fields fails
def test_register_missing_field():
    response = client.post("/register", json={
        "username": "abc",
        "password": "1234",
        # birthdate missing
        "business_type": "Self-employed",
        "business_field": "Food",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    assert response.status_code == 422

# tests if a registered user can login successfully
def test_login_success():
    username = random_username()

    # register first
    client.post("/register", json={
        "username": username,
        "password": "testpass",
        "birthdate": "1999-01-01",
        "business_type": "Self-employed",
        "business_field": "Tech",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    # login
    response = client.post("/login", json={
        "username": username,
        "password": "testpass"
    })

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "Login successful" in response.json()["message"]

# tests login with wrong password
def test_login_wrong_password():
    username = random_username()

    client.post("/register", json={
        "username": username,
        "password": "correctpass",
        "birthdate": "1999-01-01",
        "business_type": "Self-employed",
        "business_field": "Tech",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    response = client.post("/login", json={
        "username": username,
        "password": "wrongpass"
    })

    assert response.status_code == 401

# tests login with non-existing user
def test_login_user_not_found():
    response = client.post("/login", json={
        "username": "no_such_user",
        "password": "whatever"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"

# tests login when user is already connected
def test_login_already_connected():
    username = random_username()

    client.post("/register", json={
        "username": username,
        "password": "pass123",
        "birthdate": "1995-01-01",
        "business_type": "Self-employed",
        "business_field": "Tech",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })

    client.post("/login", json={
        "username": username,
        "password": "pass123"
    })

    response = client.post("/login", json={
        "username": username,
        "password": "pass123"
    })

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "User already logged in."

