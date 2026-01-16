from pymongo import MongoClient

MONGO_URI = "mongodb+srv://020696:020696@cluster0.i3kuv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

db = client["InstaAdDB"]
#collection for users
customers_collection = db["customers"]
#collection for saved ads for each user
saved_ads_collection = db["saved_ads"]
