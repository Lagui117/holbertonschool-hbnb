"""
HBnBFacade - Pattern Façade
"""
from BLL.user import User
from BLL.place import Place
from BLL.review import Review
from BLL.amenity import Amenity
from PL.in_memory_repository import InMemoryRepository



class HBnBFacade:
    """Façade orchestrant les opérations métier"""
    
    def __init__(self):
        """Initialise avec un repository"""
        self.repo = InMemoryRepository()
    
    # ==================== USERS ====================
    
    def create_user(self, data):
        """Crée un utilisateur"""
        email = data.get('email')
        if self.repo.find_by_email(email):
            raise ValueError("Email already exists")
        
        user = User(
            email=email,
            password=data.get('password'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        return self.repo.add(user)
    
    def get_user(self, user_id):
        """Récupère un utilisateur"""
        return self.repo.get(User, user_id)
    
    def get_all_users(self):
        """Liste tous les utilisateurs"""
        return self.repo.all(User)
    
    def update_user(self, user_id, data):
        """Met à jour un utilisateur"""
        user = self.repo.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        new_email = data.get('email')
        if new_email and new_email != user.email:
            existing = self.repo.find_by_email(new_email)
            if existing and existing.id != user_id:
                raise ValueError("Email already exists")
            user.email = new_email.lower().strip()
        
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        if 'password' in data:
            user.password = data['password']
        
        return self.repo.update(user)
    
    # ==================== AMENITIES ====================
    
    def create_amenity(self, data):
        """Crée un équipement"""
        amenity = Amenity(name=data.get('name'))
        return self.repo.add(amenity)
    
    def get_amenity(self, amenity_id):
        """Récupère un équipement"""
        return self.repo.get(Amenity, amenity_id)
    
    def get_all_amenities(self):
        """Liste tous les équipements"""
        return self.repo.all(Amenity)
    
    def update_amenity(self, amenity_id, data):
        """Met à jour un équipement"""
        amenity = self.repo.get(Amenity, amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        if 'name' in data:
            amenity.name = data['name'].strip()
        
        return self.repo.update(amenity)
    
    # ==================== PLACES ====================
    
    def create_place(self, data):
        """Crée un lieu"""
        owner_id = data.get('owner_id')
        if not self.repo.get(User, owner_id):
            raise ValueError("Owner not found")
        
        amenity_ids = data.get('amenity_ids', [])
        for amenity_id in amenity_ids:
            if not self.repo.get(Amenity, amenity_id):
                raise ValueError(f"Amenity {amenity_id} not found")
        
        place = Place(
            name=data.get('name'),
            owner_id=owner_id,
            price=data.get('price', 0),
            description=data.get('description', ''),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            amenity_ids=amenity_ids
        )
        return self.repo.add(place)
    
    def get_place(self, place_id):
        """Récupère un lieu"""
        return self.repo.get(Place, place_id)
    
    def get_all_places(self):
        """Liste tous les lieux"""
        return self.repo.all(Place)
    
    def update_place(self, place_id, data):
        """Met à jour un lieu"""
        place = self.repo.get(Place, place_id)
        if not place:
            raise ValueError("Place not found")
        
        if 'amenity_ids' in data:
            for amenity_id in data['amenity_ids']:
                if not self.repo.get(Amenity, amenity_id):
                    raise ValueError(f"Amenity {amenity_id} not found")
            place.amenity_ids = data['amenity_ids']
        
        if 'name' in data:
            place.name = data['name'].strip()
        if 'description' in data:
            place.description = data['description'].strip()
        if 'price' in data:
            if data['price'] < 0:
                raise ValueError("Price must be >= 0")
            place.price = float(data['price'])
        if 'latitude' in data:
            lat = data['latitude']
            if lat is not None and not (-90 <= lat <= 90):
                raise ValueError("Latitude must be between -90 and 90")
            place.latitude = lat
        if 'longitude' in data:
            lon = data['longitude']
            if lon is not None and not (-180 <= lon <= 180):
                raise ValueError("Longitude must be between -180 and 180")
            place.longitude = lon
        
        return self.repo.update(place)
    
    # ==================== REVIEWS ====================
    
    def create_review(self, data):
        """Crée un avis"""
        user_id = data.get('user_id')
        place_id = data.get('place_id')
        
        if not self.repo.get(User, user_id):
            raise ValueError("User not found")
        
        place = self.repo.get(Place, place_id)
        if not place:
            raise ValueError("Place not found")
        
        review = Review(
            text=data.get('text'),
            user_id=user_id,
            place_id=place_id
        )
        review = self.repo.add(review)
        
        # Ajouter l'ID du review au lieu
        place.reviews.append(review.id)
        self.repo.update(place)
        
        return review
    
    def get_review(self, review_id):
        """Récupère un avis"""
        return self.repo.get(Review, review_id)
    
    def get_all_reviews(self):
        """Liste tous les avis"""
        return self.repo.all(Review)
    
    def get_reviews_by_place(self, place_id):
        """Récupère les avis d'un lieu"""
        return self.repo.get_reviews_by_place(place_id)
    
    def update_review(self, review_id, data):
        """Met à jour un avis"""
        review = self.repo.get(Review, review_id)
        if not review:
            raise ValueError("Review not found")
        
        if 'text' in data:
            review.text = data['text'].strip()
        
        return self.repo.update(review)
    
    def delete_review(self, review_id):
        """Supprime un avis"""
        review = self.repo.get(Review, review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Retirer du lieu
        place = self.repo.get(Place, review.place_id)
        if place and review_id in place.reviews:
            place.reviews.remove(review_id)
            self.repo.update(place)
        
        return self.repo.delete(review)
    
    # ==================== SÉRIALISATION ÉTENDUE ====================
    
    def serialize_place_extended(self, place):
        """Sérialise un Place avec owner et amenities"""
        data = place.to_dict()
        
        # Ajouter infos propriétaire
        owner = self.repo.get(User, place.owner_id)
        if owner:
            data['owner_first_name'] = owner.first_name
            data['owner_last_name'] = owner.last_name
        
        # Ajouter détails amenities
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = self.repo.get(Amenity, amenity_id)
            if amenity:
                amenities.append(amenity.to_dict())
        data['amenities'] = amenities
        
        return data
