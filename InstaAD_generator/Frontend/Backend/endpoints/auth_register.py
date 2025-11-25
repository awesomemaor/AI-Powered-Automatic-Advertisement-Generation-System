from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Backend.endpoints.db_init import customers_collection
from bson import ObjectId

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str
    birthdate: str
    business_type: str
    business_field: str
    connected : bool 
    searched_keywords: list

@router.post("/register")
def register_user(data: RegisterRequest):

    # Check if user already exists
    if customers_collection.find_one({"username": data.username}):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    new_user = {
        "username": data.username,
        "password": data.password,   # לזכור לעשות hash בעתיד
        "birthdate": data.birthdate,
        "business_type": data.business_type,
        "business_field": data.business_field,
        "connected": False,
        "searched_keywords": [] #שמירה של מילות חיפוש
    }

    result = customers_collection.insert_one(new_user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }
