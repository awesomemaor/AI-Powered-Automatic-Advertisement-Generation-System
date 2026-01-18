def test_save_keywords_endpoint_new(client, mock_db):
    # מגדירים את DB כ-“כל המשתמשים קיימים”
    mock_db.update_one.return_value.modified_count = 1

    payload = {
        "user_id": "testuser",
        "keywords": ["ai", "ml"]
    }

    response = client.post("/save_keywords", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Keywords saved"
    assert response.json()["keywords_added"] == ["ai", "ml"]

    # בדיקה ש־DB קיבל קריאה נכונה
    mock_db.update_one.assert_called_once_with(
        {"username": "testuser"},
        {"$addToSet": {"searched_keywords": {"$each": ["ai", "ml"]}}}
    )

def test_save_keywords_endpoint_user_not_found(client, mock_db):
    # מגדירים את DB כך שהמשתמש לא קיים
    mock_db.update_one.return_value.matched_count = 0

    payload = {
        "user_id": "nonexistentuser",
        "keywords": ["ai"]
    }

    response = client.post("/save_keywords", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"

def test_save_keywords_endpoint_duplicate(client, mock_db):
    # אם המילה כבר קיימת, modified_count = 0
    mock_db.update_one.return_value.modified_count = 0

    payload = {
        "user_id": "testuser",
        "keywords": ["ai"]
    }

    response = client.post("/save_keywords", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Keywords already exist"
    assert response.json()["keywords_added"] == []

