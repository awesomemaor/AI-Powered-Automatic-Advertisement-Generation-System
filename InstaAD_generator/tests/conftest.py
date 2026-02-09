import sys
import os
import pytest
from fastapi.testclient import TestClient

# adding our frontend directory to sys.path
frontend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, frontend_root)

# import our FastAPI app
from main import app

# test client fixture for integration tests
@pytest.fixture
def client():
    return TestClient(app)

# our mongodb mock fixture for unit and integration tests
from unittest.mock import MagicMock
import builtins
import Backend.endpoints.auth_login as login_module
import Backend.endpoints.auth_register as register_module
import Backend.endpoints.generate_ad as generate_ad_module
import Backend.endpoints.save_ad as save_ad_module

@pytest.fixture
def mock_db(monkeypatch):
    mock = MagicMock()
    # this is mocking the collections used in various modules
    monkeypatch.setattr(login_module, "customers_collection", mock)
    monkeypatch.setattr(register_module, "customers_collection", mock)
    monkeypatch.setattr(generate_ad_module, "customers_collection", mock)
    return mock

@pytest.fixture
def mock_saved_ads_db(monkeypatch):
    mock = MagicMock()
    # mocking the saved_ads_collection used in save_ad module
    monkeypatch.setattr(save_ad_module, "saved_ads_collection", mock)
    return mock
