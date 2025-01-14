from pymongo.collection import Collection
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

class Category:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_category(self, category_data):
        """Insert a new category."""
        try:
            return self.collection.insert_one(category_data)
        except DuplicateKeyError:
            raise ValueError("Category with this name already exists")

    def find_all_categories(self):
        """Retrieve all categories."""
        return list(self.collection.find())
    
    def find_category_by_name(self, name):
        """Find a category by name."""
        return self.collection.find_one({"name": name})

    def delete_category(self, category_id):
        """Delete a category by ID."""
        return self.collection.delete_one({"_id": ObjectId(category_id)})