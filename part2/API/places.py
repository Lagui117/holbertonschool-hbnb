"""
API Places - Endpoints pour les lieux
"""
from flask import Blueprint, request, jsonify

places_bp = Blueprint('places', __name__)


@places_bp.route('/', methods=['GET'])
def list_places():
    """GET /api/v1/places/ - Liste tous les lieux (avec sérialisation étendue)"""
    from app import facade
    places = facade.get_all_places()
    return jsonify([facade.serialize_place_extended(p) for p in places]), 200


@places_bp.route('/', methods=['POST'])
def create_place():
    """POST /api/v1/places/ - Crée un lieu"""
    from app import facade
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        place = facade.create_place(data)
        return jsonify(facade.serialize_place_extended(place)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@places_bp.route('/<place_id>', methods=['GET'])
def get_place(place_id):
    """GET /api/v1/places/<id> - Récupère un lieu (avec sérialisation étendue)"""
    from app import facade
    place = facade.get_place(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    return jsonify(facade.serialize_place_extended(place)), 200


@places_bp.route('/<place_id>', methods=['PUT'])
def update_place(place_id):
    """PUT /api/v1/places/<id> - Met à jour un lieu"""
    from app import facade
    data = request.get_json() or {}
    
    try:
        place = facade.update_place(place_id, data)
        return jsonify(facade.serialize_place_extended(place)), 200
    except ValueError as e:
        if "not found" in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400


@places_bp.route('/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """GET /api/v1/places/<id>/reviews - Liste les avis d'un lieu"""
    from app import facade
    
    # Vérifier que le lieu existe
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    reviews = facade.get_reviews_by_place(place_id)
    return jsonify([r.to_dict() for r in reviews]), 200
