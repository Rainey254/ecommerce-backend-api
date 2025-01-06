from pymongo.collection import Collection
from bson.objectid import ObjectId
from datetime import datetime

class Notification:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_notification(self, notification_data):
        """Insert a new notification."""
        notification_data['created_at'] = datetime.now()
        notification_data['read'] = False
        return self.collection.insert_one(notification_data)

    def find_all_notifications(self, user_id):
        """Retrieve all notifications for a user."""
        return list(self.collection.find({'user_id': user_id}))

    def mark_as_read(self, notification_id):
        """Mark a notification as read."""
        return self.collection.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"read": True, "updated_at": datetime.now()}}
        )