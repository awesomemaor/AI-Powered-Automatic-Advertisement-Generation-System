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

@router.get("/get_user_preferences/{user_id}")
async def get_user_preferences(user_id: str):
    user = customers_collection.find_one(
        {"username": user_id},
        {"_id": 0, "searched_keywords": 1, "feedback_notes": 1}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "searched_keywords": user.get("searched_keywords", []),
        "feedback_notes": user.get("feedback_notes", [])
    }
