from pymongo.collection import Collection
from bson.objectid import ObjectId

class Wishlist:
    def __init__(self, collection: Collection):
        self.collection = collection

    def add_to_wishlist(self, wishlist_data):
        """Add a product to the user's wishlist."""
        return self.collection.insert_one(wishlist_data)

    def get_user_wishlist(self, user_id):
        """Retrieve the wishlist of a user."""
        return list(self.collection.find({'user_id': user_id}))

    def remove_from_wishlist(self, wishlist_id):
        """Remove a product from the wishlist."""
        return self.collection.delete_one({"_id": ObjectId(wishlist_id)})