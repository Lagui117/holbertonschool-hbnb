#!/usr/bin/env python3
"""
Script pour créer le tout premier admin
This script creates the very first admin user
"""

from app import create_app
from app.models.user import User
from app.extensions import db

def create_first_admin():
    """Crée le premier administrateur du système"""
    
    app = create_app()
    
    with app.app_context():
        # Créer toutes les tables si elles n'existent pas
        print("🔧 Creating database tables if they don't exist...")
        db.create_all()
        
        print("🔍 Checking for existing admin...")
        
        # Vérifie si un admin existe déjà
        existing_admin = User.query.filter_by(email='admin@hbnb.io').first()
        
        if existing_admin:
            print(f"⚠️  Admin already exists!")
            print(f"   Email: {existing_admin.email}")
            print(f"   ID: {existing_admin.id}")
            print(f"   Is Admin: {existing_admin.is_admin}")
            return
        
        print("✨ Creating first admin user...")
        
        # Crée le premier admin
        admin = User(
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            password='admin1234',  # Sera automatiquement hashé par User.__init__
            is_admin=True  # ✅ IMPORTANT : is_admin=True
        )
        
        # Sauvegarde dans la base de données
        db.session.add(admin)
        db.session.commit()
        
        print("✅ First admin created successfully!")
        print(f"   Email: admin@hbnb.io")
        print(f"   Password: admin1234")
        print(f"   ID: {admin.id}")
        print("\n🚀 Now you can login with these credentials!")
        print("\nExample:")
        print("curl -X POST http://127.0.0.1:5000/api/v1/auth/login \\")
        print('  -H "Content-Type: application/json" \\')
        print("  -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin1234\"}'")
        print("\n💡 Use this token in subsequent requests:")
        print('  -H "Authorization: Bearer <your_token_here>"')

if __name__ == '__main__':
    create_first_admin()