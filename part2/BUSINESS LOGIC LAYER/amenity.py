"""
Amenity - Entité équipement
"""
from .base_model import BaseModel


class Amenity(BaseModel):
    """Classe Amenity représentant un équipement"""
    
    def __init__(self, name):
        """Initialise un équipement"""
        super().__init__()
        
        if not name or not name.strip():
            raise ValueError("Amenity name is required")
        
        self.name = name.strip()
    
    def to_dict(self):
        """Convertit en dict"""
        data = super().to_dict()
        data['name'] = self.name
        return data
