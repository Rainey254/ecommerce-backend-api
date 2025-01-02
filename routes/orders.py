from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from utils.auth import check_role
from utils.db import orders_collection
from models.order import Order

orders_bp = Blueprint('orders', __name__)
order_model = Order(orders_collection)

# Place a new order
@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    user = get_jwt_identity()
    data = request.get_json()

    required_fields = ['product_id', 'quantity', 'total_price']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    # Add user-specific data
    data['user_id'] = user['_id']
    result = order_model.create_order(data)
    return jsonify({'message': 'Order placed successfully', 'order_id': str(result.inserted_id)}), 201

# Retrieve all orders (Admin only)
@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    orders = order_model.find_all_orders()
    for order in orders:
        order['_id'] = str(order['_id'])
        order['user_id'] = str(order['user_id'])
    return jsonify(orders), 200

# Retrieve user-specific orders
@orders_bp.route('/orders/user', methods=['GET'])
@jwt_required()
def get_user_orders():
    user = get_jwt_identity()
    orders = order_model.find_all_orders(user_id=user['_id'])
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders), 200

# Update an order's status (Admin only)
@orders_bp.route('/orders/<order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400

    result = order_model.update_order_status(order_id, data['status'])
    if result.matched_count == 0:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({'message': 'Order status updated successfully'}), 200

# Delete an order (Admin only)
@orders_bp.route('/orders/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    result = order_model.delete_order(order_id)
    if result.deleted_count == 0:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({'message': 'Order deleted successfully'}), 200