# app/models/base_model.py
from datetime import datetime
from app.extensions import db
from sqlalchemy import Column, DateTime

class BaseModel(db.Model):
    """
    Classe de base abstraite pour tous les modèles.
    Fournit les champs created_at / updated_at et des méthodes utilitaires.
    """
    __abstract__ = True  # Ne crée pas de table dans la base

    # Chaque modèle concret (User, Place, Review, etc.)
    # définira son propre 'id = Column(Integer, primary_key=True, autoincrement=True)'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Enregistre ou met à jour l'objet dans la base."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        """Met à jour les attributs de l'objet selon le dictionnaire donné."""
        for key, value in (data or {}).items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
