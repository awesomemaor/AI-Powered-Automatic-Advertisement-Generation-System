import pytest
from unittest.mock import MagicMock
from Backend.endpoints import auth_login, auth_register
from utils.security import hash_password

# notice that pytest fixture 'mock_db' is defined in conftest.py and will be used here

# ------------------------
# Unit tests – LOGIN
# ------------------------
def test_login_user_success(mock_db):
    # צור משתמש ב־mock DB
    hashed_pw = hash_password("1234")
    mock_db.find_one.return_value = {
        "username": "daniel",
        "password": hashed_pw,
        "connected": False
    }

    # צור אובייקט דמה ל-request
    req = type("Req", (), {"username": "daniel", "password": "1234"})()

    # הפעל את הפונקציה login
    result = auth_login.login(req)

    assert result["success"] is True
    assert "Login successful" in result["message"]

def test_login_user_already_connected(mock_db):
    hashed_pw = hash_password("1234")
    mock_db.find_one.return_value = {
        "username": "daniel",
        "password": hashed_pw,
        "connected": True
    }

    req = type("Req", (), {"username": "daniel", "password": "1234"})()

    result = auth_login.login(req)

    assert result["success"] is False
    assert "already logged in" in result["message"]

def test_login_user_wrong_password(mock_db):
    hashed_pw = hash_password("1234")
    mock_db.find_one.return_value = {
        "username": "daniel",
        "password": hashed_pw,
        "connected": False
    }

    req = type("Req", (), {"username": "daniel", "password": "wrongpass"})()

    with pytest.raises(Exception):
        auth_login.login(req)

# ------------------------
# Unit tests – REGISTER
# ------------------------
def test_register_user_success(mock_db):
    # לא קיים משתמש כזה כבר
    mock_db.find_one.return_value = None
    mock_db.insert_one.return_value.inserted_id = "fakeid123"

    req = type("Req", (), {
        "username": "newuser",
        "password": "pass1234",
        "birthdate": "2000-01-01",
        "business_type": "Self-employed",
        "business_field": "Tech",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })()

    result = auth_register.register_user(req)
    assert result["message"] == "User registered successfully"

def test_register_user_already_exists(mock_db):
    # משתמש קיים
    mock_db.find_one.return_value = {"username": "existinguser"}

    req = type("Req", (), {
        "username": "existinguser",
        "password": "pass1234",
        "birthdate": "2000-01-01",
        "business_type": "Self-employed",
        "business_field": "Tech",
        "connected": False,
        "searched_keywords": [],
        "feedback_notes": []
    })()

    with pytest.raises(Exception):
        auth_register.register_user(req)
