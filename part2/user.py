"""
User - Entité utilisateur
"""
from .base_model import BaseModel


class User(BaseModel):
    """Classe User représentant un utilisateur"""
    
    def __init__(self, email, password, first_name="", last_name=""):
        """
        Initialise un utilisateur
        
        Args:
            email: Email (obligatoire, unique)
            password: Mot de passe (obligatoire)
            first_name: Prénom
            last_name: Nom
        """
        super().__init__()
        
        if not email:
            raise ValueError("Email is required")
        if '@' not in email:
            raise ValueError("Invalid email format")
        if not password:
            raise ValueError("Password is required")
        
        self.email = email.lower().strip()
        self.password = password
        self.first_name = first_name.strip() if first_name else ""
        self.last_name = last_name.strip() if last_name else ""
    
    def to_dict(self):
        """Convertit en dict SANS le password"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        })
        return data
