import sys
import os
import pytest
from fastapi.testclient import TestClient

# מוסיף את תיקיית Frontend ל-Python path
frontend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, frontend_root)

# ייבוא האפליקציה שלנו (רק FastAPI, בלי GUI)
from main import app

@pytest.fixture
def client():
    return TestClient(app)

# Mock פשוט של DB
from unittest.mock import MagicMock
import builtins
import Backend.endpoints.auth_login as login_module
import Backend.endpoints.auth_register as register_module
import Backend.endpoints.generate_ad as generate_ad_module

@pytest.fixture
def mock_db(monkeypatch):
    mock = MagicMock()
    # מחליפים את customers_collection ב-MagicMock
    monkeypatch.setattr(login_module, "customers_collection", mock)
    monkeypatch.setattr(register_module, "customers_collection", mock)
    monkeypatch.setattr(generate_ad_module, "customers_collection", mock)
    return mock
