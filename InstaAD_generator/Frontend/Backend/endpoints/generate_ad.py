from fastapi import APIRouter, HTTPException
from Backend.endpoints.db_init import customers_collection
from pydantic import BaseModel
from bson import ObjectId

router = APIRouter()

class KeywordRequest(BaseModel):
    user_id: str
    keywords: list[str]

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str

@router.post("/save_keywords")
async def save_keywords(req: KeywordRequest):
    user_id = req.user_id
    keywords = req.keywords

    result = customers_collection.update_one(
        {"username": user_id},
        {"$addToSet": {"searched_keywords": {"$each": keywords}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="User not found")

    return {"message": "Keywords saved", "keywords_added": keywords}

@router.post("/save_feedback")
async def save_feedback(req: FeedbackRequest):
    result = customers_collection.update_one(
        {"username": req.user_id},
        {"$push": {"feedback_notes": req.feedback}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Feedback saved"}