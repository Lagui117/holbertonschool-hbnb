"""
Place Model - Modèle de données pour les lieux
Place Model - Data model for places

Ce module définit le modèle Place avec ses relations et validations
This module defines the Place model with its relationships and validations
"""

from app.extensions import db
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


# ==================== TABLE D'ASSOCIATION / ASSOCIATION TABLE ====================

# Table d'association pour la relation many-to-many entre Place et Amenity
# Association table for many-to-many relationship between Place and Amenity
place_amenity_association = Table(
    'place_amenity_association',
    db.metadata,
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
)


# ==================== MODÈLE PLACE / PLACE MODEL ====================

class Place(BaseModel, db.Model):
    """
    Modèle Place - Représente un lieu/hébergement
    Place Model - Represents a place/accommodation
    
    Relationships:
        - owner (User): Le propriétaire du lieu / The owner of the place
        - reviews (Review[]): Les avis sur ce lieu / Reviews for this place
        - amenities (Amenity[]): Les équipements du lieu / Amenities of the place
    """
    
    __tablename__ = 'places'

    # ==================== COLONNES / COLUMNS ====================
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, default=0.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # ==================== CLÉS ÉTRANGÈRES / FOREIGN KEYS ====================
    
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # ==================== RELATIONS / RELATIONSHIPS ====================
    
    # Relation avec User (propriétaire du lieu)
    # Relationship with User (place owner)
    owner = relationship('User', back_populates='places', lazy=True)

    # Relation avec Review (avis sur le lieu)
    # Relationship with Review (reviews for the place)
    reviews = relationship('Review', back_populates='place', lazy=True, cascade='all, delete-orphan')

    # Relation many-to-many avec Amenity (équipements du lieu)
    # Many-to-many relationship with Amenity (place amenities)
    amenities = relationship(
        'Amenity',
        secondary=place_amenity_association,
        back_populates='places',
        lazy='select'  # ✅ Changé de True à 'select' pour plus de contrôle
    )

    # ==================== CONSTRUCTEUR / CONSTRUCTOR ====================
    
    def __init__(self, title, description, price, latitude, longitude, owner_id=None, owner=None):
        """
        Initialise un nouveau Place
        Initialize a new Place
        
        Args:
            title (str): Titre du lieu / Place title
            description (str): Description du lieu / Place description
            price (float): Prix par nuit / Price per night
            latitude (float): Latitude (-90 à 90) / Latitude (-90 to 90)
            longitude (float): Longitude (-180 à 180) / Longitude (-180 to 180)
            owner_id (int, optional): ID du propriétaire / Owner ID
            owner (User, optional): Objet User propriétaire / Owner User object
        """
        # Appel du constructeur parent (BaseModel)
        # Call parent constructor (BaseModel)
        super().__init__()
        
        # Initialisation des attributs
        # Initialize attributes
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        # ✅ Gestion de owner_id et owner
        # Handle owner_id and owner
        if owner:
            # Si un objet owner est fourni, utilise son ID
            # If an owner object is provided, use its ID
            self.owner = owner
            self.owner_id = owner.id
        elif owner_id:
            # Sinon, utilise directement l'owner_id fourni
            # Otherwise, use the provided owner_id directly
            self.owner_id = owner_id
        else:
            # ✅ IMPORTANT : owner_id est requis
            # IMPORTANT: owner_id is required
            raise ValueError("owner_id or owner must be provided")

        # ✅ CORRECTION : Ne pas initialiser reviews et amenities ici
        # FIX: Don't initialize reviews and amenities here
        # SQLAlchemy gère ces listes automatiquement via les relationships
        # SQLAlchemy handles these lists automatically via relationships
        # self.reviews = []  # ❌ À ENLEVER
        # self.amenities = []  # ❌ À ENLEVER

        # Validation des attributs
        # Validate attributes
        self.validate_attributes()

    # ==================== VALIDATIONS ====================
    
    def validate_attributes(self):
        """
        Valide tous les attributs du Place
        Validates all Place attributes
        
        Raises:
            ValueError: Si un attribut est invalide / If an attribute is invalid
        """
        # Validation du titre
        # Title validation
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        
        # Validation de la description
        # Description validation
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        
        # Validation du prix
        # Price validation
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a non-negative number")
        
        # Validation de la latitude
        # Latitude validation
        if not isinstance(self.latitude, (int, float)) or not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be a number between -90 and 90")
        
        # Validation de la longitude
        # Longitude validation
        if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")  # ✅ Corrigé "et" → "and"

    # ==================== MÉTHODES / METHODS ====================
    
    def add_review(self, review):
        """
        Ajoute un avis au lieu
        Add a review to the place
        
        Args:
            review (Review): L'avis à ajouter / The review to add
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Ajoute un équipement au lieu
        Add an amenity to the place
        
        Args:
            amenity (Amenity): L'équipement à ajouter / The amenity to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    # ==================== REPRÉSENTATION / REPRESENTATION ====================
    
    def __repr__(self):
        """
        Représentation string du Place pour le debug
        String representation of Place for debugging
        """
        return f"<Place id={self.id} title='{self.title}' owner_id={self.owner_id}>"
