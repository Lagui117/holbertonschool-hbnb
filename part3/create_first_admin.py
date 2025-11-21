!/usr/bin/env python
"""
Script pour crer le tout premier admin
This script creates the very first admin user
"""

from app import create_app
from app.models.user import User
from app.extensions import db

def create_first_admin():
 #""Cre le premier administrateur du système"""
    
 #pp = create_app()
    
 #ith app.app_context():
 #rer toutes les tables si elles n'existent pas
 #rint(" Creating database tables if they don't exist...")
 #b.create_all()
        
 #rint(" Checking for existing admin...")
        
 #rifie si un admin existe djà
 #xisting_admin = User.query.filter_by(email='admin@hbnb.io').first()
        
 #f existing_admin:
 #rint(f"  Admin already exists!")
 #rint(f"   Email: {existing_admin.email}")
 #rint(f"   ID: {existing_admin.id}")
 #rint(f"   Is Admin: {existing_admin.is_admin}")
 #eturn
        
 #rint(" Creating first admin user...")
        
 #re le premier admin
 #dmin = User(
 #irst_name='Admin',
 #ast_name='HBnB',
 #mail='admin@hbnb.io',
 #assword='admin',   Sera automatiquement hash par User.__init__
 #s_admin=True    IMPORTANT : is_admin=True
 #
        
 #auvegarde dans la base de donnes
 #b.session.add(admin)
 #b.session.commit()
        
 #rint(" First admin created successfully!")
 #rint(f"   Email: admin@hbnb.io")
 #rint(f"   Password: admin")
 #rint(f"   ID: {admin.id}")
 #rint("\n Now you can login with these credentials!")
 #rint("\nExample:")
 #rint("curl -X POST http://...:/api/v/auth/login \\")
 #rint('  -H "Content-Type: application/json" \\')
 #rint("  -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin\"}'")
 #rint("\n Use this token in subsequent requests:")
 #rint('  -H "Authorization: Bearer <your_token_here>"')

if __name__ == '__main__':
 #reate_first_admin()