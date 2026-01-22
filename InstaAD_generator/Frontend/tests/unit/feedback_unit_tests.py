import pytest
from unittest.mock import MagicMock
from Backend.endpoints.generate_ad import save_feedback, FeedbackRequest, get_user_preferences
import Backend.endpoints.generate_ad as generate_module
from fastapi import HTTPException

# testing successful feedback saving
@pytest.mark.asyncio
async def test_save_feedback_success(mock_db):
    # existing user
    mock_db.update_one.return_value.matched_count = 1

    req = FeedbackRequest(
        user_id="daniel",
        feedback="Great ad quality!"
    )

    result = await save_feedback(req)

    mock_db.update_one.assert_called_once_with(
        {"username": "daniel"},
        {"$push": {"feedback_notes": "Great ad quality!"}}
    )

    assert result["message"] == "Feedback saved"

# testing user not found case
@pytest.mark.asyncio
async def test_save_feedback_user_not_found(mock_db):
    # user לא קיים
    mock_db.update_one.return_value.matched_count = 0

    req = FeedbackRequest(
        user_id="unknown_user",
        feedback="Nice video"
    )

    with pytest.raises(HTTPException) as exc:
        await save_feedback(req)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

    mock_db.update_one.assert_called_once()

# testing to get the user preferences
@pytest.mark.asyncio
async def test_get_user_preferences_success(mock_db):
    mock_db.find_one.return_value = {
        "searched_keywords": ["ai", "ml"],
        "feedback_notes": ["nice ad", "too long"]
    }

    result = await get_user_preferences("daniel")

    mock_db.find_one.assert_called_once_with(
        {"username": "daniel"},
        {"_id": 0, "searched_keywords": 1, "feedback_notes": 1}
    )

    assert result["searched_keywords"] == ["ai", "ml"]
    assert result["feedback_notes"] == ["nice ad", "too long"]

# testing user not found case
@pytest.mark.asyncio
async def test_get_user_preferences_user_not_found(mock_db):
    mock_db.find_one.return_value = None

    with pytest.raises(HTTPException) as exc:
        await get_user_preferences("unknown")

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"