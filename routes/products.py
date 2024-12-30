from flask import Blueprint, request, jsonify
from utils.auth import check_role
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import products_collection
from models.product import Product

products_bp = Blueprint('products', __name__)
product_model = Product(products_collection)

#create a product
@products_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    required_fields = ['name', 'description', 'price', 'stock', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400
    
    result = product_model.create(data)
    return jsonify({'message': 'Product created', 'id': str(result.inserted_id)}), 201

# Get all products
@products_bp.route('/products', methods=['GET'])
def get_all_products():
    products = product_model.find_all()
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products), 200

# Get a product by ID
@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = product_model.find_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    product['_id'] = str(product['_id'])
    return jsonify(product), 200

# Update a product
@products_bp.route('/products/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    result = product_model.update(product_id, data)
    if result.matched_count == 0:
        return jsonify({'error': 'product not found'}), 404
    
    return jsonify({'message': 'Product updated successfully'}), 200

#Delete a product
@products_bp.route('/products/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403
    
    result = product_model.delete(product_id)
    if result.deleted_count == 0:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({'message': 'product deleted successfully'}), 200