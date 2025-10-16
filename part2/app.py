"""
Application Flask principale - HBnB Partie 2
"""
from flask import Flask
from FACADE.facade import HBnBFacade

# Créer l'application Flask
app = Flask(__name__)

# Initialiser la façade (globale)
facade = HBnBFacade()

# Importer et enregistrer les blueprints
from API.users import users_bp
from API.amenities import amenities_bp
from API.places import places_bp
from API.reviews import reviews_bp


app.register_blueprint(users_bp, url_prefix='/api/v1/users')
app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')
app.register_blueprint(places_bp, url_prefix='/api/v1/places')
app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')


@app.route('/')
def index():
    """Route racine"""
    return {
        'message': 'HBnB API - Partie 2',
        'endpoints': {
            'users': '/api/v1/users',
            'amenities': '/api/v1/amenities',
            'places': '/api/v1/places',
            'reviews': '/api/v1/reviews'
        }
    }


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 HBnB API - Partie 2")
    print("=" * 70)
    print("📍 API : http://127.0.0.1:5000")
    print("📍 Endpoints :")
    print("   • Users     : /api/v1/users")
    print("   • Amenities : /api/v1/amenities")
    print("   • Places    : /api/v1/places")
    print("   • Reviews   : /api/v1/reviews")
    print("=" * 70)
    print("💡 Testez avec cURL ! Voir TESTING_GUIDE.md")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)