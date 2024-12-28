from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["ecommerce"]

users_collection = db["users"]
products_collection = db["products"]

#testing the connection
def test_db():
    try:
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

# Fetch al users
def get_all_users():
    return list(users_collection.find())

# Insert new user to database
def inser_user(user_data):
    users_collection.insert_one(user_data)

test_db()