"""
API Reviews - Endpoints pour les avis
"""
from flask import Blueprint, request, jsonify

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/', methods=['GET'])
def list_reviews():
    """GET /api/v1/reviews/ - Liste tous les avis"""
    from app import facade
    reviews = facade.get_all_reviews()
    return jsonify([r.to_dict() for r in reviews]), 200


@reviews_bp.route('/', methods=['POST'])
def create_review():
    """POST /api/v1/reviews/ - Crée un avis"""
    from app import facade
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        review = facade.create_review(data)
        return jsonify(review.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@reviews_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    """GET /api/v1/reviews/<id> - Récupère un avis"""
    from app import facade
    review = facade.get_review(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    return jsonify(review.to_dict()), 200


@reviews_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id):
    """PUT /api/v1/reviews/<id> - Met à jour un avis"""
    from app import facade
    data = request.get_json() or {}
    
    try:
        review = facade.update_review(review_id, data)
        return jsonify(review.to_dict()), 200
    except ValueError as e:
        if "not found" in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400


@reviews_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """DELETE /api/v1/reviews/<id> - Supprime un avis (SEULE entité avec DELETE)"""
    from app import facade
    
    try:
        facade.delete_review(review_id)
        return '', 204  # No Content
    except ValueError as e:
        return jsonify({'error': str(e)}), 404