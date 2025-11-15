# app/models/user.py
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel
import re
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates, relationship
from sqlalchemy.sql import expression


class User(BaseModel):
    """
    Modèle User : représente un utilisateur dans la base de données.
    Hérite de BaseModel (timestamps + méthodes save/update).
    """
    __tablename__ = 'users'

    # ID entier auto-incrémenté
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Champs de base
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Rôle (admin ou user)
    is_admin = Column(Boolean, nullable=False,
                      server_default=expression.false(),  # Défaut côté DB
                      default=False)                      # Défaut côté ORM

    # Relations avec d'autres modèles
    places = relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='user', lazy=True)

    # ----------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        """
        Si 'password' est fourni en clair, il est automatiquement hashé.
        Si c'est déjà un hash bcrypt (commence par '$2'), on le garde tel quel.
        """
        raw_pw = kwargs.get('password')
        if raw_pw is not None and not str(raw_pw).startswith('$2'):
            kwargs['password'] = bcrypt.generate_password_hash(raw_pw).decode('utf-8')
        super().__init__(*args, **kwargs)
        self.validate()

    # ----------------------------------------------------------------------

    @validates('email')
    def validate_email(self, key, email):
        """Vérifie le format de l'email avant insertion."""
        if not self.is_valid_email(email):
            raise ValueError("Invalid email format")
        return email

    def validate(self):
        """Validation des champs obligatoires."""
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name must be between 1 and 50 characters")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name must be between 1 and 50 characters")
        if not self.is_valid_email(self.email):
            raise ValueError("Invalid email format")

    @staticmethod
    def is_valid_email(email):
        """Regex de validation email."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email or '') is not None

    # ----------------------------------------------------------------------

    def set_password(self, password_plain: str):
        """
        Hash un mot de passe en clair.
        Utilisez cette méthode uniquement pour changer le mot de passe
        d'un utilisateur existant.
        """
        if not str(password_plain).strip():
            raise ValueError("Empty password")
        self.password = bcrypt.generate_password_hash(password_plain).decode('utf-8')

    def verify_password(self, password_plain: str) -> bool:
        """Vérifie un mot de passe contre le hash stocké."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password_plain)

    # ----------------------------------------------------------------------

    def __repr__(self):
        return f"<User {self.email}>"