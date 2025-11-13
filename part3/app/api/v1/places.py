"""
API Places - Endpoints pour la gestion des lieux
API Places - Endpoints for place management

Ce module gère les opérations CRUD pour les lieux (places) avec authentification JWT
This module handles CRUD operations for places with JWT authentication
"""
import logging
from flask_restx import Namespace, Resource, fields
from app.api.v1 import facade  # Import the shared facade instance
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# Configuration du logger pour le debugging
# Logger configuration for debugging
logger = logging.getLogger(__name__)

# Création du namespace pour regrouper les routes des places
# Create namespace to group place routes
api = Namespace('places', description='Place operations')


# ==================== MODÈLES DE DONNÉES / DATA MODELS ====================

# Modèle pour la création d'un place (tous les champs requis)
# Model for creating a place (all required fields)
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Modèle pour la mise à jour d'un place (tous les champs optionnels)
# Model for updating a place (all fields optional)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})


# ==================== ROUTES COLLECTION /places/ ====================

@api.route('/')
class PlaceList(Resource):
    """
    Gestion de la collection de places
    Handles the collection of places
    """
    
    # ==================== POST - Créer un place ====================
    
    @api.doc('create_place', security='Bearer')  # ✅ Affiche le cadenas 🔒 dans Swagger
    @jwt_required()  # ✅ Authentification JWT requise
    @api.expect(place_model)  # Définit le format attendu pour la requête
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    def post(self):
        """
        Register a new place
        Créer un nouveau lieu
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Le owner_id est automatiquement défini à partir du token JWT
        The owner_id is automatically set from the JWT token
        
        Restrictions:
            - Seuls les utilisateurs authentifiés peuvent créer des places
            - Only authenticated users can create places
        
        Returns:
            201: Place créé avec succès / Place successfully created
            400: Données invalides / Invalid input data
            401: Token JWT manquant ou invalide / Missing or invalid JWT token
        """
        # Récupération de l'identité de l'utilisateur authentifié depuis le JWT
        # Get the authenticated user's identity from JWT
        current_user = get_jwt_identity()
        
        # Récupération des données JSON de la requête
        # Get JSON data from the request
        place_data = api.payload

        try:
            # ✅ SÉCURITÉ : Le owner_id est forcé à l'ID de l'utilisateur authentifié
            # SECURITY: Force owner_id to the authenticated user's ID
            # Cela empêche un utilisateur de créer un place au nom d'un autre
            # This prevents a user from creating a place on behalf of another user
            place_data['owner_id'] = current_user['id']

            # Création du place via la facade (gère les validations métier)
            # Create place through facade (handles business validations)
            new_place = facade.create_place(place_data)

            # Retour du place créé avec status 201 (Created)
            # Return created place with status 201 (Created)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,
                'amenities': [amenity.id for amenity in new_place.amenities]
            }, 201
            
        except ValueError as e:
            # Erreur de validation (ex: prix négatif, coordonnées invalides)
            # Validation error (e.g., negative price, invalid coordinates)
            logger.error(f"Validation error while creating place: {str(e)}")
            return {'error': str(e)}, 400
        
        except Exception as e:
            # Erreur inattendue
            # Unexpected error
            logger.error(f"Unexpected error while creating place: {str(e)}")
            return {'error': 'Internal server error'}, 500

    # ==================== GET - Lister tous les places ====================
    
    @api.doc('list_places')  # Pas de security='Bearer' car endpoint public
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places
        Récupérer la liste de tous les lieux
        
        Authentification requise : NON (endpoint public)
        Authentication required: NO (public endpoint)
        
        Returns:
            200: Liste de tous les places / List of all places
        
        Example response:
            [
                {
                    "id": 1,
                    "title": "Beach House",
                    "description": "Beautiful beach house",
                    "price": 100.0,
                    "latitude": 45.5,
                    "longitude": -73.6,
                    "owner_id": 2,
                    "amenities": [1, 3, 5]
                },
                ...
            ]
        """
        # Récupération de tous les places via la facade
        # Retrieve all places through the facade
        places = facade.get_all_places()
        
        # Sérialisation de chaque place en dictionnaire
        # Serialize each place to dictionary
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,
            'amenities': [amenity.id for amenity in place.amenities]
        } for place in places], 200


# ==================== ROUTES RESSOURCE /places/<place_id> ====================

@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Gestion d'un place spécifique
    Handles a specific place
    """
    
    # ==================== GET - Récupérer un place ====================
    
    @api.doc('get_place')  # Pas de security='Bearer' car endpoint public
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID
        Obtenir les détails d'un lieu par son ID
        
        Authentification requise : NON (endpoint public)
        Authentication required: NO (public endpoint)
        
        Args:
            place_id (int): ID du place / Place ID
        
        Returns:
            200: Détails du place / Place details
            404: Place non trouvé / Place not found
        """
        # Recherche du place par son ID
        # Search for place by ID
        place = facade.get_place(place_id)
        
        # Si le place n'existe pas, retour 404
        # If place doesn't exist, return 404
        if not place:
            return {'error': 'Place not found'}, 404

        # Retour des détails du place avec status 200
        # Return place details with status 200
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,
            'amenities': [amenity.id for amenity in place.amenities]
        }, 200

    # ==================== PUT - Mettre à jour un place ====================
    
    @api.doc('update_place', security='Bearer')  # ✅ Affiche le cadenas 🔒
    @jwt_required()  # ✅ Authentification JWT requise
    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action - You are not the owner')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    def put(self, place_id):
        """
        Update a place's information
        Mettre à jour les informations d'un lieu
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Restrictions:
            - Seul le propriétaire du place peut le modifier
            - Only the place owner can update it
            - EXCEPTION : Les admins peuvent modifier n'importe quel place
            - EXCEPTION: Admins can update any place
        
        Args:
            place_id (int): ID du place à modifier / Place ID to update
        
        Returns:
            200: Place mis à jour / Place updated successfully
            403: Non autorisé (pas le propriétaire) / Unauthorized (not the owner)
            404: Place non trouvé / Place not found
            400: Données invalides / Invalid input data
        """
        # Récupération de l'identité de l'utilisateur authentifié
        # Get the authenticated user's identity
        current_user = get_jwt_identity()
        
        # Récupération des claims JWT (contient is_admin, etc.)
        # Get JWT claims (contains is_admin, etc.)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        try:
            # Vérification de l'existence du place
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': "Place not found"}, 404
            
            # ✅ CONTRÔLE D'ACCÈS / ACCESS CONTROL
            # Vérifier que l'utilisateur est soit :
            # Check that the user is either:
            # 1. Le propriétaire du place (owner)
            # 2. Un administrateur (admin bypass)
            if not is_admin and str(place.owner.id) != current_user['id']:
                logger.warning(
                    f"Unauthorized update attempt on place {place_id} "
                    f"by user {current_user['id']}"
                )
                return {'error': "Unauthorized action"}, 403

            # Récupération des données de mise à jour
            # Get update data
            update_data = api.payload
            logger.debug(f"Updating place {place_id} with data: {update_data}")

            # Mise à jour du place via la facade
            # Update place through facade
            updated_place = facade.update_place(place_id, update_data)
            
            # Retour du place mis à jour avec status 200
            # Return updated place with status 200
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner.id,
                'amenities': [amenity.id for amenity in updated_place.amenities]
            }, 200

        except ValueError as e:
            # Erreur de validation métier
            # Business validation error
            logger.error(f"Validation error while updating place: {str(e)}")
            return {'error': str(e)}, 400
        
        except Exception as e:
            # Erreur inattendue
            # Unexpected error
            logger.error(f"Unexpected error while updating place: {str(e)}")
            return {'error': "Internal server error"}, 500

    # ==================== DELETE - Supprimer un place ====================
    
    @api.doc('delete_place', security='Bearer')  # ✅ Affiche le cadenas 🔒
    @jwt_required()  # ✅ Authentification JWT requise
    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    @api.response(403, "Unauthorized action - You are not the owner")
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    def delete(self, place_id):
        """
        Delete a place
        Supprimer un lieu
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Restrictions:
            - Seul le propriétaire du place peut le supprimer
            - Only the place owner can delete it
            - EXCEPTION : Les admins peuvent supprimer n'importe quel place
            - EXCEPTION: Admins can delete any place
        
        Args:
            place_id (int): ID du place à supprimer / Place ID to delete
        
        Returns:
            200: Place supprimé / Place deleted successfully
            403: Non autorisé (pas le propriétaire) / Unauthorized (not the owner)
            404: Place non trouvé / Place not found
        """
        # Récupération de l'identité de l'utilisateur authentifié
        # Get the authenticated user's identity
        current_user = get_jwt_identity()
        
        # Récupération des claims JWT
        # Get JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        try:
            # Vérification de l'existence du place
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': "Place not found"}, 404
            
            # ✅ CONTRÔLE D'ACCÈS / ACCESS CONTROL
            # Vérifier que l'utilisateur est soit le propriétaire soit admin
            # Check that the user is either the owner or admin
            if not is_admin and str(place.owner.id) != current_user['id']:
                logger.warning(
                    f"Unauthorized deletion attempt on place {place_id} "
                    f"by user {current_user['id']}"
                )
                return {'error': "Unauthorized action"}, 403

            logger.debug(f"Deleting place {place_id}")

            # Suppression du place via la facade
            # Delete place through facade
            facade.delete_place(place_id)
            
            # Retour message de succès avec status 200
            # Return success message with status 200
            return {'message': "Place deleted successfully"}, 200
        
        except Exception as e:
            # Erreur inattendue
            # Unexpected error
            logger.error(f"Unexpected error while deleting a place: {str(e)}")
            return {'error': "Internal server error"}, 500