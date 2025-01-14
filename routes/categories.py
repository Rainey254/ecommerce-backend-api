from flask import Blueprint, request, jsonify
from utils.db import categories_collection
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth import check_role, get_token_from_request
from models.category import Category

categories_bp = Blueprint('categories', __name__)
category_model = Category(categories_collection)

# Create a category (Admin only)
@categories_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    token = get_token_from_request()
    if not check_role(token, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    required_fields = ['name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Category name is required'}), 400

    result = category_model.create_category(data)
    return jsonify({'message': 'Category created', 'id': str(result.inserted_id)}), 201

# Get all categories
@categories_bp.route('/categories', methods=['GET'])
def get_all_categories():
    categories = category_model.find_all_categories()
    for category in categories:
        category['_id'] = str(category['_id'])
    return jsonify(categories), 200

# Delete a category (Admin only)
@categories_bp.route('/categories/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    token = get_token_from_request()
    if not check_role(token, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    result = category_model.delete_category(category_id)
    if result.deleted_count == 0:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({'message': 'Category deleted successfully'}), 200