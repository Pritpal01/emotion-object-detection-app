
from pymongo import MongoClient

client = MongoClient("")
db = client["emotion_app"]
users_col = db["users"]
emotions_col = db["emotions"]
