from pymongo import MongoClient

MONGO_URI = "mongodb+srv://020696:020696@cluster0.i3kuv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

db = client["InstaAdDB"]
customers_collection = db["customers"]
