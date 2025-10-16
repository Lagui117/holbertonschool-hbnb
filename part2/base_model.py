"""
BaseModel - Classe de base pour toutes les entités
"""
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """Classe de base avec attributs communs (UUID, timestamps)"""
    
    def __init__(self):
        """Initialise avec un UUID et les timestamps"""
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Met à jour le timestamp de modification"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
