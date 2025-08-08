
from pymongo import MongoClient

client = MongoClient("mongodb+srv://users:emotions@cluster1.xwnrllv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["emotion_app"]
users_col = db["users"]
emotions_col = db["emotions"]
