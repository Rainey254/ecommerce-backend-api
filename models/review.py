from pymongo.collection import Collection
from bson.objectid import ObjectId
from datetime import datetime

class Review:
    def __init__(self, collection: Collection):
        self.collection = collection

    def add_review(self, review_data):
        """Insert a new review."""
        review_data['created_at'] = datetime.now()
        return self.collection.insert_one(review_data)

    def find_reviews_by_product(self, product_id):
        """Retrieve all reviews for a specific product."""
        return list(self.collection.find({'product_id': product_id}))

    def find_reviews_by_user(self, user_id):
        """Retrieve all reviews made by a specific user."""
        return list(self.collection.find({'user_id': user_id}))