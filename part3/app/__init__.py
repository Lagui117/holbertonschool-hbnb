from flask import Flask, redirect
from flask_restx import Api
from flask_cors import CORS
from app.persistence.repository import SQLAlchemyRepository
from app.extensions import db, bcrypt, jwt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protector import api as protected_ns
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load the configuration
    app.config.from_object(config_class)
    
    # Enable CORS for frontend communication
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Database tables will be created
        db.create_all()

    #  Configuration JWT pour Swagger UI (ajoute le bouton Authorize)
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT Authorization header using the Bearer scheme. \n\n"
                          "Enter: **'Bearer &lt;token&gt;'**\n\n"
                          "Example: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'"
        }
    }

    # Initialize Flask-RESTX API avec JWT authorizations
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API with JWT Authentication', 
        doc='/',  # Documentation Swagger à la racine
        authorizations=authorizations,  #  Active les autorisations JWT
        security='Bearer'  #  Active la sécurité JWT par défaut
    )

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protector')

    return app