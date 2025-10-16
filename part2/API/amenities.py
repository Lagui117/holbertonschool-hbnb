"""
API Amenities - Endpoints pour les équipements
"""
from flask import Blueprint, request, jsonify

amenities_bp = Blueprint('amenities', __name__)


@amenities_bp.route('/', methods=['GET'])
def list_amenities():
    """GET /api/v1/amenities/ - Liste tous les équipements"""
    from app import facade
    amenities = facade.get_all_amenities()
    return jsonify([a.to_dict() for a in amenities]), 200


@amenities_bp.route('/', methods=['POST'])
def create_amenity():
    """POST /api/v1/amenities/ - Crée un équipement"""
    from app import facade
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        amenity = facade.create_amenity(data)
        return jsonify(amenity.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@amenities_bp.route('/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """GET /api/v1/amenities/<id> - Récupère un équipement"""
    from app import facade
    amenity = facade.get_amenity(amenity_id)
    
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    
    return jsonify(amenity.to_dict()), 200


@amenities_bp.route('/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """PUT /api/v1/amenities/<id> - Met à jour un équipement"""
    from app import facade
    data = request.get_json() or {}
    
    try:
        amenity = facade.update_amenity(amenity_id, data)
        return jsonify(amenity.to_dict()), 200
    except ValueError as e:
        if "not found" in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400
    