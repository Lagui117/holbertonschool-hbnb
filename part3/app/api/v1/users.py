"""
API Users - Endpoints pour la gestion des utilisateurs
API Users - Endpoints for user management

Ce module gère les opérations CRUD pour les utilisateurs avec authentification JWT et RBAC
This module handles CRUD operations for users with JWT authentication and RBAC
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.api.v1 import facade  # Import du module façade partagé

# Création du namespace pour regrouper les routes des users
# Create namespace to group user routes
api = Namespace('users', description='User operations')


# ==================== MODÈLES DE DONNÉES / DATA MODELS ====================

# Modèle pour la création d'un utilisateur (inscription)
# Model for user creation (registration)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin privileges (default: False, only admins can set to True)')  # ✅ AJOUT
})

# Modèle pour la mise à jour d'un utilisateur
# Model for user update
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})


# ==================== HELPERS / FONCTIONS UTILITAIRES ====================

def is_admin_user():
    """
    Récupère la claim is_admin dans le JWT
    Get the is_admin claim from JWT
    
    Returns:
        bool: True si l'utilisateur est admin, False sinon
              True if user is admin, False otherwise
    """
    claims = get_jwt()
    return claims.get('is_admin', False)


def _current_user_id():
    """
    Retourne l'ID utilisateur courant sous forme de string
    Returns current user ID as string
    
    Returns:
        str: ID de l'utilisateur authentifié / Authenticated user ID
    """
    return str(get_jwt_identity())


# ==================== ROUTES COLLECTION /users/ ====================

@api.route('/')
class UserList(Resource):
    """
    Gestion de la collection d'utilisateurs
    Handles the collection of users
    """
    
    # ==================== POST - Créer un utilisateur ====================
    
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Forbidden - Only admins can create admin users')
    def post(self):
        """
        Register a new user
        Inscription publique : création d'un utilisateur
        
        Authentification requise : NON (endpoint public pour inscription)
        Authentication required: NO (public endpoint for registration)
        
        Restrictions:
            - Tout le monde peut créer un utilisateur standard (is_admin=False)
            - Anyone can create a standard user (is_admin=False)
            - SEULS les admins authentifiés peuvent créer des admins (is_admin=True)
            - ONLY authenticated admins can create admin users (is_admin=True)
        
        Returns:
            201: Utilisateur créé avec succès / User successfully created
            400: Email déjà enregistré / Email already registered
            403: Interdit - Seuls les admins peuvent créer des admins
                 Forbidden - Only admins can create admin users
        
        Example request (standard user):
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "password": "secret123"
            }
        
        Example request (admin user - requires admin JWT):
            {
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@hbnb.com",
                "password": "admin123",
                "is_admin": true
            }
        """
        # Récupération des données JSON de la requête
        # Get JSON data from the request
        user_data = api.payload
        
        # Récupère is_admin du payload (défaut: False si non fourni)
        # Get is_admin from payload (default: False if not provided)
        is_admin_requested = user_data.get('is_admin', False)
        
        # ✅ CONTRÔLE DE SÉCURITÉ / SECURITY CHECK
        # Si is_admin=True est demandé, vérifier que le demandeur est un admin authentifié
        # If is_admin=True is requested, verify that requester is an authenticated admin
        if is_admin_requested:
            try:
                # Tente de vérifier le JWT
                # Try to verify JWT
                jwt_required()(lambda: None)()
                
                # Vérifie si l'utilisateur courant est admin
                # Check if current user is admin
                if not is_admin_user():
                    return {
                        'error': 'Only admins can create admin users'
                    }, 403
                    
            except Exception:
                # Pas de token JWT valide = pas autorisé à créer un admin
                # No valid JWT token = not allowed to create admin
                return {
                    'error': 'Authentication required to create admin users'
                }, 403
        
        try:
            # Création de l'utilisateur via la facade
            # Create user through facade
            new_user = facade.create_user({
                'email': user_data['email'],
                'password': user_data['password'],
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'is_admin': is_admin_requested  # ✅ Passe le flag admin
            })
            
            # Retour succès avec status 201 (Created)
            # Return success with status 201 (Created)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
            
        except ValueError as e:
            # Erreur de validation (ex: email déjà existant)
            # Validation error (e.g., email already exists)
            return {'error': str(e)}, 400
    
    # ==================== GET - Lister tous les utilisateurs ====================
    
    @api.doc('list_users', security='Bearer')  # ✅ Affiche le cadenas 🔒
    @jwt_required()  # ✅ JWT requis
    @api.response(200, 'List of users retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    @api.response(403, 'Forbidden - Admin access required')
    def get(self):
        """
        List all users (admin only)
        Lister tous les utilisateurs (admin uniquement)
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Restrictions:
            - ADMIN UNIQUEMENT / ADMIN ONLY
            - Seuls les administrateurs peuvent voir la liste complète des utilisateurs
            - Only administrators can see the complete list of users
        
        Returns:
            200: Liste des utilisateurs / List of users
            401: Non authentifié / Unauthorized
            403: Accès refusé (pas admin) / Forbidden (not admin)
        """
        # ✅ VÉRIFICATION ADMIN / ADMIN CHECK
        if not is_admin_user():
            return {
                'error': 'Admin access required'
            }, 403
        
        # Récupération de tous les utilisateurs via la facade
        # Get all users through facade
        users = facade.get_all_users()
        
        # Sérialisation de la liste des utilisateurs
        # Serialize user list
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        } for user in users], 200


# ==================== ROUTES RESSOURCE /users/<user_id> ====================

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Gestion d'un utilisateur spécifique
    Handles a specific user
    """
    
    # ==================== GET - Obtenir un utilisateur ====================
    
    @api.doc('get_user', security='Bearer')  # ✅ Affiche le cadenas 🔒
    @jwt_required()  # ✅ JWT requis
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    @api.response(403, 'Forbidden - Can only access own data unless admin')
    def get(self, user_id):
        """
        Get user details by ID (self or admin)
        Obtenir les infos d'un utilisateur (self ou admin)
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Restrictions:
            - Les utilisateurs peuvent voir leurs propres infos
            - Users can view their own information
            - Les admins peuvent voir les infos de n'importe qui
            - Admins can view anyone's information
        
        Args:
            user_id (int): ID de l'utilisateur / User ID
        
        Returns:
            200: Détails de l'utilisateur / User details
            403: Accès refusé / Forbidden
            404: Utilisateur non trouvé / User not found
        """
        # Récupération de l'utilisateur
        # Get the user
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # ✅ CONTRÔLE D'ACCÈS / ACCESS CONTROL
        # Autoriser si : l'utilisateur accède à ses propres données OU est admin
        # Allow if: user accessing own data OR is admin
        current_id = _current_user_id()
        if str(user_id) != current_id and not is_admin_user():
            return {
                'error': 'Access denied. You can only view your own profile.'
            }, 403
        
        # Retour des détails de l'utilisateur
        # Return user details
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200
    
    # ==================== PUT - Mettre à jour un utilisateur ====================
    
    @api.doc('update_user', security='Bearer')  # ✅ Affiche le cadenas 🔒
    @jwt_required()  # ✅ JWT requis
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    @api.response(403, 'Forbidden - Can only update own data unless admin')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update user information (self or admin)
        Mettre à jour ses infos (self ou admin)
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Restrictions:
            - Les utilisateurs peuvent modifier leurs propres infos
            - Users can update their own information
            - Les admins peuvent modifier les infos de n'importe qui
            - Admins can update anyone's information
        
        Args:
            user_id (int): ID de l'utilisateur / User ID
        
        Returns:
            200: Utilisateur mis à jour / User updated successfully
            403: Accès refusé / Forbidden
            404: Utilisateur non trouvé / User not found
            400: Données invalides / Invalid input data
        """
        # Récupération de l'utilisateur
        # Get the user
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # ✅ CONTRÔLE D'ACCÈS / ACCESS CONTROL
        current_id = _current_user_id()
        if str(user_id) != current_id and not is_admin_user():
            return {
                'error': 'Access denied. You can only update your own profile.'
            }, 403
        
        # Récupération des données de mise à jour
        # Get update data
        update_data = api.payload
        
        try:
            # Mise à jour via la facade
            # Update through facade
            updated_user = facade.update_user(user_id, update_data)
            
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
    
    # ==================== DELETE - Supprimer un utilisateur ====================
    
    @api.doc('delete_user', security='Bearer')  # ✅ Affiche le cadenas 🔒
    @jwt_required()  # ✅ JWT requis
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(401, 'Unauthorized - Missing or invalid JWT token')
    @api.response(403, 'Forbidden - Can only delete own account unless admin')
    def delete(self, user_id):
        """
        Delete a user (self or admin)
        Supprimer un utilisateur (self ou admin)
        
        Authentification requise : OUI (JWT Bearer token)
        Authentication required: YES (JWT Bearer token)
        
        Restrictions:
            - Les utilisateurs peuvent supprimer leur propre compte
            - Users can delete their own account
            - Les admins peuvent supprimer n'importe quel compte
            - Admins can delete any account
        
        Args:
            user_id (int): ID de l'utilisateur / User ID
        
        Returns:
            200: Utilisateur supprimé / User deleted successfully
            403: Accès refusé / Forbidden
            404: Utilisateur non trouvé / User not found
        """
        # Récupération de l'utilisateur
        # Get the user
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # ✅ CONTRÔLE D'ACCÈS / ACCESS CONTROL
        current_id = _current_user_id()
        if str(user_id) != current_id and not is_admin_user():
            return {
                'error': 'Access denied. You can only delete your own account.'
            }, 403
        
        # Suppression via la facade
        # Delete through facade
        facade.delete_user(user_id)
        
        return {
            'message': 'User deleted successfully'
        }, 200