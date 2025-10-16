"""
Review - Entité avis
"""
from .base_model import BaseModel


class Review(BaseModel):
    """Classe Review représentant un avis"""
    
    def __init__(self, text, user_id, place_id):
        """Initialise un avis"""
        super().__init__()
        
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty")
        if not user_id:
            raise ValueError("User ID is required")
        if not place_id:
            raise ValueError("Place ID is required")
        
        self.text = text.strip()
        self.user_id = user_id
        self.place_id = place_id
    
    def to_dict(self):
        """Convertit en dict"""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        return data