import pytest
from unittest.mock import MagicMock
from Backend.endpoints import generate_ad as generate_module
from Backend.endpoints.generate_ad import save_keywords, KeywordRequest


def test_save_keywords_new_user(mock_db):
    # הגדרת המשתמש הקיים
    mock_db.update_one.return_value.modified_count = 1

    req = KeywordRequest(user_id="daniel", keywords=["tech", "ai"])
    result = save_keywords(req)

    # בדיקה שעדכון DB קרה
    mock_db.update_one.assert_called_once_with(
        {"username": "daniel"},
        {"$addToSet": {"searched_keywords": {"$each": ["tech", "ai"]}}}
    )

    # בדיקה שהפלט נכון
    assert result["message"] == "Keywords saved"
    assert result["keywords_added"] == ["tech", "ai"]

def test_save_keywords_user_not_found(mock_db):
    # אם המשתמש לא קיים
    mock_db.update_one.return_value.modified_count = 0

    req = KeywordRequest(user_id="unknown", keywords=["tech", "ai"])
    
    with pytest.raises(Exception) as e_info:
        save_keywords(req)

    mock_db.update_one.assert_called_once()
    assert "User not found" in str(e_info.value)

def test_save_keywords_duplicate(mock_db):
    # אם המילה כבר קיימת, $addToSet לא משנה את modified_count
    mock_db.update_one.return_value.modified_count = 1

    req = KeywordRequest(user_id="daniel", keywords=["tech"])
    result = save_keywords(req)

    mock_db.update_one.assert_called_once()
    # הפלט צריך להיות עדיין אותו דבר
    assert result["keywords_added"] == ["tech"]
