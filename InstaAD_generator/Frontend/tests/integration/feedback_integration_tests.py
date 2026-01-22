def test_save_feedback_success(client, mock_db):
    # מדמים משתמש קיים
    mock_db.update_one.return_value.matched_count = 1

    response = client.post("/save_feedback", json={
        "user_id": "daniel",
        "feedback": "Great ad"
    })

    mock_db.update_one.assert_called_once_with(
        {"username": "daniel"},
        {"$push": {"feedback_notes": "Great ad"}}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Feedback saved"

def test_save_feedback_user_not_found(client, mock_db):
    mock_db.update_one.return_value.matched_count = 0

    response = client.post("/save_feedback", json={
        "user_id": "unknown",
        "feedback": "Nice"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_user_preferences_success(client, mock_db):
    mock_db.find_one.return_value = {
        "searched_keywords": ["ai", "marketing"],
        "feedback_notes": ["Nice video"]
    }

    response = client.get("/get_user_preferences/daniel")

    mock_db.find_one.assert_called_once_with(
        {"username": "daniel"},
        {"_id": 0, "searched_keywords": 1, "feedback_notes": 1}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["searched_keywords"] == ["ai", "marketing"]
    assert data["feedback_notes"] == ["Nice video"]

def test_get_user_preferences_user_not_found(client, mock_db):
    mock_db.find_one.return_value = None

    response = client.get("/get_user_preferences/unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
