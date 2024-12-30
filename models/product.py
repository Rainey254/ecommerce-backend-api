from pymongo.collection import Collection
from bson.objectid import ObjectId

class Product:
    def __init__(self, collection: Collection):
        self.Collection = collection

    def create(self, product_data):
        """insert a new product"""
        return self.collection.insert_one(product_data)
    
    def find_all(self):
        """Retrieve all products."""
        return list(self.collection.find())
    
    def find_by_id(self, product_id):
        """Retrieve a product by id"""
        return self.collection.find_one({"_id": ObjectId(product_id)})
    
    def update(self, product_id, update_data):
        """Update a product by id."""
        return self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    
    def delete(self, product_id):
        """Deletes a product by ID"""
        return self.collection.delete_one({"_id": ObjectId(product_id)})