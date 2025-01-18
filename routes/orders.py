from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from utils.auth import check_role, get_token_from_request
from utils.db import orders_collection
from models.order import Order
from models.user import UserModel

orders_bp = Blueprint('orders', __name__)
order_model = Order(orders_collection)

# Place a new order
@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    try:
        user = get_jwt_identity()
        if isinstance(user, str):
            user = UserModel.get_user_by_id(user)
        data = request.get_json()

        required_fields = ['product_id', 'quantity', 'total_price']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        # Add user-specific data
        data['user_id'] = user['_id']
        result = order_model.create_order(data)
        return jsonify({'message': 'Order placed successfully', 'order_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Retrieve all orders (Admin only)
@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    token = get_token_from_request()
    if not check_role(token, 'admin'):
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
    try:
        user = get_jwt_identity()
        print("JWT Identity:", user)

        user_id = user
        print("Fetching orders for User ID:", user_id)

        orders = order_model.find_all_orders(user_id=user)
        for order in orders:
            if '_id' in order:
                order['_id'] = str(order['_id'])
        return jsonify(orders), 200
    except Exception as e:
         print("Error in get_user_orders:", str(e))
         return jsonify({'error': str(e)}), 500


# Update an order's status (Admin only)
@orders_bp.route('/orders/<order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    token = get_token_from_request()
    if not check_role(token, 'admin'):
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
    token = get_token_from_request()
    if not check_role(token, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    result = order_model.delete_order(order_id)
    if result.deleted_count == 0:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({'message': 'Order deleted successfully'}), 200