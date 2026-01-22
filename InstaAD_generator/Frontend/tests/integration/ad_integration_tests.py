def test_save_ad_success(client, mock_saved_ads_db):
    mock_saved_ads_db.find_one.return_value = None

    response = client.post("/save-ad", json={
        "username": "daniel",
        "task_id": "task123",
        "video_url": "http://video.com/1.mp4"
    })

    mock_saved_ads_db.insert_one.assert_called_once()

    assert response.status_code == 200
    assert response.json()["message"] == "Ad saved successfully"


def test_save_ad_duplicate(client, mock_saved_ads_db):
    mock_saved_ads_db.find_one.return_value = {"_id": "existing"}

    response = client.post("/save-ad", json={
        "username": "daniel",
        "task_id": "task123",
        "video_url": "http://video.com/1.mp4"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "This video is already saved"

from bson import ObjectId
from datetime import datetime


def test_get_ads_success(client, mock_saved_ads_db):
    mock_saved_ads_db.find.return_value = [
        {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "video_url": "http://video.com/1.mp4",
            "saved_at": datetime(2024, 1, 1)
        }
    ]

    response = client.get("/get-ads/daniel")

    assert response.status_code == 200
    ads = response.json()["ads"]

    assert len(ads) == 1
    assert ads[0]["video_url"] == "http://video.com/1.mp4"
    assert isinstance(ads[0]["_id"], str)
    assert isinstance(ads[0]["saved_at"], str)


def test_get_ads_empty(client, mock_saved_ads_db):
    mock_saved_ads_db.find.return_value = []

    response = client.get("/get-ads/daniel")

    assert response.status_code == 200
    assert response.json()["ads"] == []


def test_delete_ad_success(client, mock_saved_ads_db):
    mock_saved_ads_db.delete_one.return_value.deleted_count = 1

    response = client.delete("/delete-ad/507f1f77bcf86cd799439011")

    assert response.status_code == 200
    assert response.json()["message"] == "Ad deleted"


def test_delete_ad_not_found(client, mock_saved_ads_db):
    mock_saved_ads_db.delete_one.return_value.deleted_count = 0

    response = client.delete("/delete-ad/507f1f77bcf86cd799439011")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ad not found"


