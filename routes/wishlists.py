from flask import Blueprint, request, jsonify
from utils.db import wishlists_collection, products_collection
from models.wishlist import Wishlist
from models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity

wishlists_bp = Blueprint('wishlists', __name__)
wishlist_model = Wishlist(wishlists_collection)

# Add to wishlist
@wishlists_bp.route('/wishlist', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    user = get_jwt_identity()
    data = request.get_json()
    data['user_id'] = user

    result = wishlist_model.add_to_wishlist(data)
    return jsonify({'message': 'Product added to wishlist', 'id': str(result.inserted_id)}), 201

# Get user's wishlist
@wishlists_bp.route('/wishlist', methods=['GET'])
@jwt_required()
def get_user_wishlist():
    user = get_jwt_identity()
    wishlist = wishlist_model.get_user_wishlist(user)
    product_model = Product(products_collection)
    enriched_wishlist = []
    for item in wishlist:
        item['_id'] = str(item['_id'])
        product_details = product_model.find_by_id(item['product_id'])
        if product_details:
            product_details['_id'] = str(product_details['_id'])
            item['product_details'] = product_details

        enriched_wishlist.append(item)
    return jsonify(wishlist), 200

# Remove from wishlist
@wishlists_bp.route('/wishlist/<wishlist_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(wishlist_id):
    result = wishlist_model.remove_from_wishlist(wishlist_id)
    if result.deleted_count == 0:
        return jsonify({'error': 'Item not found'}), 404

    return jsonify({'message': 'Item removed from wishlist'}), 200