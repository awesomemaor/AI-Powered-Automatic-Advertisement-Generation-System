import uuid
import pytest
from Backend.endpoints import auth_login as login_module
from Backend.endpoints import auth_register as register_module
from utils.security import hash_password
from unittest.mock import MagicMock

# -------- Helpers --------
def random_username():
    return f"user_{uuid.uuid4().hex[:8]}"

# -------------------
# Integration tests using client + mock_db
# -------------------

def test_register_success(client, mock_db):
    username = random_username()

    # מגדירים שהמשתמש לא קיים
    mock_db.find_one.return_value = None
    # insert_one מחזיר MagicMock עם inserted_id
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "mocked_id_123"
    mock_db.insert_one.return_value = mock_insert_result

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
    assert "user_id" in response.json()

def test_register_existing_user(client, mock_db):
    username = random_username()

    # מגדירים שהמשתמש כבר קיים
    mock_db.find_one.return_value = {"username": username}

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

def test_register_missing_field(client, mock_db):
    # לא צריך לגעת ב-DB כאן
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

def test_login_success(client, mock_db):
    username = random_username()
    hashed_pw = hash_password("testpass")

    # מגדירים שהמשתמש קיים ב-db
    mock_db.find_one.return_value = {
        "username": username,
        "password": hashed_pw,
        "connected": False
    }

    response = client.post("/login", json={
        "username": username,
        "password": "testpass"
    })

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "Login successful" in response.json()["message"]

def test_login_wrong_password(client, mock_db):
    username = random_username()
    hashed_pw = hash_password("correctpass")

    mock_db.find_one.return_value = {
        "username": username,
        "password": hashed_pw,
        "connected": False
    }

    response = client.post("/login", json={
        "username": username,
        "password": "wrongpass"
    })

    assert response.status_code == 401

def test_login_user_not_found(client, mock_db):
    # משתמש לא קיים
    mock_db.find_one.return_value = None

    response = client.post("/login", json={
        "username": "no_such_user",
        "password": "whatever"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"

def test_login_already_connected(client, mock_db):
    username = random_username()
    hashed_pw = hash_password("pass123")

    # מחזירים שהמשתמש מחובר כבר
    mock_db.find_one.return_value = {
        "username": username,
        "password": hashed_pw,
        "connected": True
    }

    response = client.post("/login", json={
        "username": username,
        "password": "pass123"
    })

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["message"] == "User already logged in."
