from pymongo.collection import Collection
from bson.objectid import ObjectId

class Category:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_category(self, category_data):
        """Insert a new category."""
        return self.collection.insert_one(category_data)

    def find_all_categories(self):
        """Retrieve all categories."""
        return list(self.collection.find())

    def delete_category(self, category_id):
        """Delete a category by ID."""
        return self.collection.delete_one({"_id": ObjectId(category_id)})