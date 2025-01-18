from flask import Blueprint, request, jsonify
from models.user import UserModel
from utils.auth import hash_password, verify_password, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)
user_model = UserModel()

@users_bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    required_fields = ['email', 'password', 'name']

    # Check for missing fields
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    # Check if email already exists
    if user_model.get_user_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 409

    # Hash the password
    data['password'] = hash_password(data['password'])
    user_id = user_model.create_user(data)
    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

@users_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = user_model.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    del user['password']  # Don't expose the password
    return jsonify(user), 200

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = user_model.list_users()
    for user in users:
        user['_id'] = str(user['_id'])
        del user['password']  # Don't expose passwords
    return jsonify(users), 200

@users_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    success = user_model.update_user(user_id, data)
    if not success:
        return jsonify({'error': 'User not found or update failed'}), 400
    return jsonify({'message': 'User updated successfully'}), 200

@users_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    success = user_model.delete_user(user_id)
    if not success:
        return jsonify({'error': 'User not found or deletion failed'}), 400
    return jsonify({'message': 'User deleted successfully'}), 200