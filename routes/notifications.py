from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import notifications_collection
from models.notification import Notification

notifications_bp = Blueprint('notifications', __name__)
notification_model = Notification(notifications_collection)

# Create a notification
@notifications_bp.route('/notifications', methods=['POST'])
@jwt_required()
def create_notification():
    data = request.get_json()
    required_fields = ['user_id', 'message']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    result = notification_model.create_notification(data)
    return jsonify({'message': 'Notification created', 'id': str(result.inserted_id)}), 201

# Get all notifications for a user
@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_user_notifications():
    user = get_jwt_identity()
    notifications = notification_model.find_all_notifications(user)
    for notification in notifications:
        notification['_id'] = str(notification['_id'])
    return jsonify(notifications), 200

# Mark a notification as read
@notifications_bp.route('/notifications/<notification_id>', methods=['PUT'])
@jwt_required()
def mark_notification_as_read(notification_id):
    result = notification_model.mark_as_read(notification_id)
    if result.matched_count == 0:
        return jsonify({'error': 'Notification not found'}), 404

    return jsonify({'message': 'Notification marked as read'}), 200