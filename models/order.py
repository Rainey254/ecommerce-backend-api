from pymongo.collection import Collection
from bson.objectid import ObjectId
from datetime import datetime

class Order:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_order(self, order_data):
        """Insert a new order into the collection."""
        order_data['created_at'] = datetime.now()
        order_data['status'] = 'Pending'
        return self.collection.insert_one(order_data)

    def find_all_orders(self, user_id=None):
        """Retrieve all orders, optionally filtered by user ID."""
        if user_id:
            return list(self.collection.find({'user_id': user_id}))
        return list(self.collection.find())

    def find_order_by_id(self, order_id):
        """Retrieve an order by its ID."""
        return self.collection.find_one({"_id": ObjectId(order_id)})

    def update_order_status(self, order_id, status):
        """Update the status of an order."""
        return self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )

    def delete_order(self, order_id):
        """Delete an order by ID."""
        return self.collection.delete_one({"_id": ObjectId(order_id)})