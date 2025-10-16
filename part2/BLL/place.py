"""
Place - Entité lieu/hébergement
"""
from .base_model import BaseModel


class Place(BaseModel):
    """Classe Place représentant un lieu"""
    
    def __init__(self, name, owner_id, price=0, description="", 
                 latitude=None, longitude=None, amenity_ids=None):
        """Initialise un lieu"""
        super().__init__()
        
        if not name or not name.strip():
            raise ValueError("Place name is required")
        if not owner_id:
            raise ValueError("Owner ID is required")
        if price < 0:
            raise ValueError("Price must be >= 0")
        
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        self.name = name.strip()
        self.owner_id = owner_id
        self.price = float(price)
        self.description = description.strip() if description else ""
        self.latitude = float(latitude) if latitude is not None else None
        self.longitude = float(longitude) if longitude is not None else None
        self.amenity_ids = amenity_ids if amenity_ids else []
        self.reviews = []
    
    def to_dict(self):
        """Convertit en dict"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenity_ids': self.amenity_ids
        })
        return data
