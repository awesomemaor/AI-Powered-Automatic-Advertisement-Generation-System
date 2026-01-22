import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException

from Backend.endpoints.save_ad import (
    save_ad,
    get_ads,
    delete_ad,
    SaveAdRequest
)

def test_save_ad_success(mock_saved_ads_db):
    mock_saved_ads_db.find_one.return_value = None

    data = SaveAdRequest(
        username="daniel",
        task_id="task123",
        video_url="http://video.com/1.mp4"
    )

    result = save_ad(data)

    mock_saved_ads_db.insert_one.assert_called_once()
    assert result["message"] == "Ad saved successfully"


def test_save_ad_duplicate(mock_saved_ads_db):
    # mocking as if the ad already exists and it found in DB
    mock_saved_ads_db.find_one.return_value = {"_id": "existing"}

    data = SaveAdRequest(
        username="daniel",
        task_id="task123",
        video_url="http://video.com/1.mp4"
    )

    with pytest.raises(HTTPException) as exc:
        save_ad(data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "This video is already saved"


def test_get_ads_success(mock_saved_ads_db):
    mock_saved_ads_db.find.return_value = [
        {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "video_url": "http://video.com/1.mp4",
            "saved_at": datetime(2024, 1, 1)
        }
    ]

    result = get_ads("daniel")
    ads = result["ads"]

    assert len(ads) == 1
    assert ads[0]["video_url"] == "http://video.com/1.mp4"
    assert isinstance(ads[0]["_id"], str)
    assert isinstance(ads[0]["saved_at"], str)


def test_get_ads_empty(mock_saved_ads_db):
    mock_saved_ads_db.find.return_value = []

    result = get_ads("daniel")

    assert result["ads"] == []


def test_delete_ad_success(mock_saved_ads_db):
    mock_saved_ads_db.delete_one.return_value.deleted_count = 1

    result = delete_ad("507f1f77bcf86cd799439011")

    assert result["message"] == "Ad deleted"


def test_delete_ad_not_found(mock_saved_ads_db):
    mock_saved_ads_db.delete_one.return_value.deleted_count = 0

    with pytest.raises(HTTPException) as exc:
        delete_ad("507f1f77bcf86cd799439011")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Ad not found"
