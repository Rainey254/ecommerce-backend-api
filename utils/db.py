import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["ecommerce"]

users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]
notifications_collection = db["notifications"]
reviews_collection = db["reviews"]
categories_collection = db["categories"]
audit_logs_collection = db["auditlogs"]
wishlists_collection = db["wishlists"]

categories_collection.create_index([("name", ASCENDING)], unique=True)

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