# app/api/v1/users.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.api.v1 import facade  # Import du module façade partagé

api = Namespace('users', description='User operations')

# Modèle pour la documentation Swagger et la validation d'entrée
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def is_admin_user():
    """Récupère la claim is_admin dans le JWT."""
    claims = get_jwt()
    return claims.get('is_admin', False)


def _current_user_id():
    """Retourne l'ID utilisateur courant sous forme de string."""
    return str(get_jwt_identity())


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------

@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    @jwt_required()
    def get(self):
        """Lister tous les utilisateurs (admin uniquement)."""
        if not is_admin_user():
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """
        Inscription publique : création d'un utilisateur standard (is_admin=False).
        Pas de JWT requis.
        """
        user_data = request.get_json() or {}

        # Ne jamais faire confiance au client pour le rôle
        user_data.pop('is_admin', None)

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User successfully created'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    def get(self, id):
        """Obtenir les infos d'un utilisateur (self ou admin)."""
        current_id = _current_user_id()
        admin = is_admin_user()

        if not admin and current_id != str(id):
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, "You cannot modify email or password")
    @api.response(403, "Unauthorized action")
    def put(self, id):
        """Mettre à jour ses infos (self ou admin)."""
        current_id = _current_user_id()
        admin = is_admin_user()

        if not admin and current_id != str(id):
            return {'error': "Unauthorized action"}, 403

        update_data = request.get_json() or {}

        # Un utilisateur normal ne peut pas changer email ou password
        if not admin and ('email' in update_data or 'password' in update_data):
            return {'error': "You cannot modify email or password"}, 400

        updated_user = facade.update_user(id, update_data)
        if not updated_user:
            return {'error': "User not found"}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

    @jwt_required()
    @api.response(200, "User successfully deleted")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    def delete(self, id):
        """Supprimer un utilisateur (self ou admin)."""
        current_id = _current_user_id()
        admin = is_admin_user()

        # Vérifier si c'est l'utilisateur lui-même ou un admin
        if not admin and current_id != str(id):
            return {'error': "Unauthorized action"}, 403

        deleted = facade.delete_user(id)
        if not deleted:
            return {'error': "User not found"}, 404

        return {'message': "User successfully deleted"}, 200