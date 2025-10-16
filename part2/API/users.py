"""
API Users - Endpoints pour les utilisateurs
"""
from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
def list_users():
    """GET /api/v1/users/ - Liste tous les utilisateurs"""
    from app import facade
    users = facade.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


@users_bp.route('/', methods=['POST'])
def create_user():
    """POST /api/v1/users/ - Crée un utilisateur"""
    from app import facade
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        user = facade.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """GET /api/v1/users/<id> - Récupère un utilisateur"""
    from app import facade
    user = facade.get_user(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT /api/v1/users/<id> - Met à jour un utilisateur"""
    from app import facade
    data = request.get_json() or {}
    
    try:
        user = facade.update_user(user_id, data)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        if "not found" in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400
    