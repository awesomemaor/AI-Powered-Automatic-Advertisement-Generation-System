from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from .db_init import customers_collection  # Import your MongoDB collection
from utils.security import hash_password,verify_password

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LogoutRequest(BaseModel):
    username: str

@router.post("/login")
def login(req: LoginRequest):
    print(f"Received login request: username={req.username}, password={req.password}")
    
    user = customers_collection.find_one({"username": req.username})
    print(f"MongoDB query result: {user}")
    
    if user:
        stored_pw = user.get("password", "")
        # if password is hashed with Argon2
        if stored_pw.startswith("$argon2"):  
            print("Stored password is hashed with Argon2")
            if verify_password(req.password, user["password"]):
                print("Password matched")
                if user["connected"]:
                    return {"success": False, "message": "User already logged in."}
                
                customers_collection.update_one(
                    {"username": req.username},
                    {"$set": {"connected": True}}
                )

                return {"success": True, "message": "Login successful!", "username": req.username}
            else:
                print("Incorrect password or username")
                raise HTTPException(status_code=401, detail="Incorrect password")
        # if stored password is in plain text, migrate to Argon2
        elif req.password == stored_pw:
            print("Password matched (plain text)")
            # updating the password to Argon2 hash
            new_hashed = hash_password(req.password)
            customers_collection.update_one(
                {"username": req.username},
                {"$set": {"password": new_hashed}}
            )
            print("Password migrated to Argon2 hash")

            if user["connected"]:
                return {"success": False, "message": "User already logged in."}
            customers_collection.update_one(
                {"username": req.username},
                {"$set": {"connected": True}}
            )
            return {"success": True, "message": "Login successful!", "username": req.username}

        else:
            print("Incorrect password or username")
            raise HTTPException(status_code=401, detail="User not found")
    else:
        print("Incorrect password or username")
        raise HTTPException(status_code=401, detail="User not found")

@router.post("/logout")
def logout_user(req: LogoutRequest):
    customers_collection.update_one(
        {"username": req.username},
        {"$set": {"connected": False}}
    )
    return {"success": True, "message": "Logout successful!"}