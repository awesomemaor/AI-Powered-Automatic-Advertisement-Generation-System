def test_save_keywords_endpoint_new(client, mock_db):
    # Mocking successful bulk_write execution
    mock_db.bulk_write.return_value.matched_count = 1
    mock_db.bulk_write.return_value.modified_count = 1

    payload = {
        "user_id": "testuser",
        "keywords": ["ai", "ml"]
    }

    response = client.post("/save_keywords", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Keywords saved"
    assert response.json()["keywords_added"] == ["ai", "ml"]

    # Verify bulk_write was used
    mock_db.bulk_write.assert_called_once()

def test_save_keywords_endpoint_user_not_found(client, mock_db):
    # Mocking user not found (matched_count = 0)
    mock_db.bulk_write.return_value.matched_count = 0

    payload = {
        "user_id": "nonexistentuser",
        "keywords": ["ai"]
    }

    response = client.post("/save_keywords", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"

def test_save_keywords_endpoint_duplicate(client, mock_db):
    # Mocking duplicate keywords (user found, but no modification)
    mock_db.bulk_write.return_value.matched_count = 1
    mock_db.bulk_write.return_value.modified_count = 0

    payload = {
        "user_id": "testuser",
        "keywords": ["ai"]
    }

    response = client.post("/save_keywords", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Keywords already exist"
    assert response.json()["keywords_added"] == []