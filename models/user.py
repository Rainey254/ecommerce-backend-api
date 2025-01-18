from utils.db import users_collection
from bson.objectid import ObjectId

class UserModel:
    @staticmethod
    def create_user(user_data):
        """
        Create a new user.
        :param user_data: Dictionary containing user details.
        :return: Inserted user's ID as a string.
        """
        result = users_collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        :param user_id: String ID of the user.
        :return: User document as a dictionary, or None if not found.
        """
        try:
            return users_collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by their email.
        :param email: Email address of the user.
        :return: User document as a dictionary, or None if not found.
        """
        return users_collection.find_one({"email": email})

    @staticmethod
    def update_user(user_id, update_data):
        """
        Update user details.
        :param user_id: String ID of the user to update.
        :param update_data: Dictionary of fields to update.
        :return: Boolean indicating if the update was successful.
        """
        try:
            result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
            return result.modified_count > 0
        except Exception:
            return False

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user by their ID.
        :param user_id: String ID of the user.
        :return: Boolean indicating if the deletion was successful.
        """
        try:
            result = users_collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    @staticmethod
    def list_users(filters=None):
        """
        Retrieve all users or filter by criteria.
        :param filters: Dictionary of filters (optional).
        :return: List of user documents.
        """
        filters = filters or {}
        return list(users_collection.find(filters))









