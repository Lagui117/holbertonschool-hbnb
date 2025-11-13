#!/usr/bin/env python3
"""
Script pour créer le tout premier admin
This script creates the very first admin user
"""

from app import create_app
from app.models.user import User
from app.extensions import db, bcrypt

def create_first_admin():
    """Crée le premier administrateur du système"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking for existing admin...")
        
        # Vérifie si un admin existe déjà
        existing_admin = User.query.filter_by(email='admin@hbnb.com').first()
        
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
            last_name='HBNB',
            email='admin@hbnb.com',
            is_admin=True  # ✅ IMPORTANT : is_admin=True
        )
        
        # Hash le mot de passe
        admin.password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        
        # Sauvegarde dans la base de données
        db.session.add(admin)
        db.session.commit()
        
        print("✅ First admin created successfully!")
        print(f"   Email: admin@hbnb.com")
        print(f"   Password: admin123")
        print(f"   ID: {admin.id}")
        print("\n🚀 Now you can login with these credentials!")
        print("\nExample:")
        print("curl -X POST http://127.0.0.1:5000/api/v1/auth/login \\")
        print('  -H "Content-Type: application/json" \\')
        print("  -d '{\"email\": \"admin@hbnb.com\", \"password\": \"admin123\"}'")

if __name__ == '__main__':
    create_first_admin()