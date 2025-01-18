from flask import Blueprint, request, jsonify
from utils.db import reviews_collection
from models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_bp = Blueprint('reviews', __name__)
review_model = Review(reviews_collection)

# Add a review
@reviews_bp.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    user = get_jwt_identity()
    data = request.get_json()

    required_fields = ['product_id', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    data['user_id'] = user
    result = review_model.add_review(data)
    return jsonify({'message': 'Review added', 'id': str(result.inserted_id)}), 201

# Get reviews by product
@reviews_bp.route('/reviews/product/<product_id>', methods=['GET'])
@jwt_required()
def get_reviews_by_product(product_id):
    reviews = review_model.find_reviews_by_product(product_id)
    for review in reviews:
        review['_id'] = str(review['_id'])
    return jsonify(reviews), 200

# Get reviews by user
@reviews_bp.route('/reviews/user', methods=['GET'])
@jwt_required()
def get_reviews_by_user():
    user = get_jwt_identity()
    reviews = review_model.find_reviews_by_user(user)
    for review in reviews:
        review['_id'] = str(review['_id'])
    return jsonify(reviews), 200