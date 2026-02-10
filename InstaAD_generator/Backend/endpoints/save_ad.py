from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from Backend.endpoints.db_init import saved_ads_collection

router = APIRouter()

class SaveAdRequest(BaseModel):
    username: str
    task_id: str
    video_url: str

@router.post("/save-ad")
def save_ad(data: SaveAdRequest):

    # אחר כך לשנות חזרה שלא יהיה קומנט זה רק בשביל דיבאג
    # check if ad already saved
    existing_ad = saved_ads_collection.find_one({
        "username": data.username,
        "video_url": data.video_url
    })

    if existing_ad:
        raise HTTPException(
            status_code=400,
            detail="This video is already saved"
        )

    # if ad not saved, save it
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

@router.get("/get-ads/{username}")
def get_ads(username: str):
    ads = list(saved_ads_collection.find(
        {"username": username},
        {"_id": 1, "video_url": 1, "saved_at": 1}
    ))

    # המרה של ObjectId ל-string
    for ad in ads:
        ad["_id"] = str(ad["_id"])
        ad["saved_at"] = ad["saved_at"].isoformat()

    return {"ads": ads}

@router.delete("/delete-ad/{ad_id}")
def delete_ad(ad_id: str):
    result = saved_ads_collection.delete_one(
        {"_id": ObjectId(ad_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ad not found")

    return {"message": "Ad deleted"}

