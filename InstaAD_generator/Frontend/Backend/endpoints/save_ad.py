from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Backend.endpoints.db_init import saved_ads_collection

router = APIRouter()

class SaveAdRequest(BaseModel):
    username: str
    task_id: str
    video_url: str

@router.post("/save-ad")
def save_ad(data: SaveAdRequest):
    ad_data = {
        "username": data.username,
        "task_id": data.task_id,
        "video_url": data.video_url,
        "saved_at": datetime.utcnow()
    }

    saved_ads_collection.insert_one(ad_data)

    return {
        "message": "Ad saved successfully"
    }
