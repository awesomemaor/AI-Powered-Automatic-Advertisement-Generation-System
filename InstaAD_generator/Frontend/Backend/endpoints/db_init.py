from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["InstaAdDB"]
#collection for users
customers_collection = db["customers"]
#collection for saved ads for each user
saved_ads_collection = db["saved_ads"]
