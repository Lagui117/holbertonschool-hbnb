# app/service/facade.py
import logging
from app.extensions import db
from app.persistence.user_repository import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HBnBFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # Repos
            self.user_repo = UserRepository()
            self.place_repo = SQLAlchemyRepository(Place)
            self.amenity_repo = SQLAlchemyRepository(Amenity)
            self.review_repo = SQLAlchemyRepository(Review)
            self._initialized = True

    # ----------------------------------------------------------------------
    # USERS
    # ----------------------------------------------------------------------

    def create_user(self, user_data: dict):
        """
        Crée un utilisateur (user standard ou admin selon is_admin).
        - Le flag is_admin doit être validé au niveau de l'endpoint (api/v1/users.py).
        - Le modèle User hash déjà le password en __init__ si on passe un mot de passe en clair.
        """
        logger.debug(f"Creating user with data: {user_data}")

        # Champs autorisés à la création
        safe = {
            k: v for k, v in (user_data or {}).items()
            if k in {'first_name', 'last_name', 'email', 'password', 'is_admin'}
        }

        # Par défaut, is_admin = False si non spécifié
        if 'is_admin' not in safe:
            safe['is_admin'] = False

        try:
            user = self.user_repo.create(**safe)
            logger.debug(f"User created with ID: {user.id}, is_admin: {user.is_admin}")
            return user
        except ValueError as e:
            logger.error(f"Error creating user: {e}")
            raise

    def get_user(self, user_id):
        logger.debug(f"Looking for user with ID: {user_id}")
        user = self.user_repo.get_by_id(user_id)
        if user:
            logger.debug(f"Found user: {user.first_name} {user.last_name}")
        else:
            logger.debug("User not found")
        return user

    def get_user_by_email(self, email):
        logger.debug(f"Looking for user with email: {email}")
        user = self.user_repo.get_by_email(email)
        if user:
            logger.debug(f"Found user: {user.first_name} {user.last_name}")
        else:
            logger.debug("User not found")
        return user

    def get_all_users(self):
        """Retrieve all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data: dict):
        """
        Met à jour un user (self/admin). On interdit toute modif de is_admin ici.
        On ne traite ici QUE first_name / last_name (le reste est géré ailleurs).
        """
        try:
            if not user_data:
                return self.user_repo.get_by_id(user_id)

            data = dict(user_data)
            # Interdictions
            data.pop('is_admin', None)
            data.pop('email', None)
            data.pop('password', None)

            allowed = {k: v for k, v in data.items() if k in {'first_name', 'last_name'}}
            if not allowed:
                # Rien à mettre à jour -> retourne l'utilisateur tel quel
                return self.user_repo.get_by_id(user_id)

            user = self.user_repo.update(user_id, allowed)
            return user
        except ValueError as e:
            logger.error(f"Error updating user: {e}")
            raise

    def delete_user(self, user_id):
        """
        Supprime un utilisateur par son ID.
        Retourne True si la suppression a réussi, False sinon.
        """
        logger.debug(f"Attempting to delete user with ID: {user_id}")
        try:
            self.user_repo.delete(user_id)
            logger.debug(f"User {user_id} successfully deleted")
            return True
        except ValueError as e:
            logger.error(f"Error deleting user: {e}")
            return False

    # (optionnel) Promotion admin — à appeler uniquement depuis une route admin
    def promote_user_to_admin(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        user.is_admin = True
        db.session.commit()
        return user

    # ----------------------------------------------------------------------
    # AMENITIES
    # ----------------------------------------------------------------------

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        if len(amenity_data.get('name', '')) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        if 'name' in amenity_data and len(amenity_data['name']) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        amenity = self.get_amenity(amenity_id)
        if amenity:
            self.amenity_repo.update(amenity_id, amenity_data)
            return amenity
        return None

    # ----------------------------------------------------------------------
    # PLACES
    # ----------------------------------------------------------------------

    def create_place(self, place_data):
        logger.debug(f"Attempting to create place with data: {place_data}")

        data = dict(place_data or {})
        owner_id = data.pop('owner_id', None)
        amenities_ids = data.pop('amenities', [])

        if not owner_id:
            raise ValueError("owner_id is required")

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"User with id {owner_id} not found")

        try:
            place = Place(**data, owner=owner)

            for amenity_id in amenities_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
                else:
                    logger.warning(f"Amenity {amenity_id} not found")

            self.place_repo.add(place)
            logger.debug(f"Place added to repository with owner {owner.id}")
            return place

        except Exception as e:
            logger.error(f"Error creating place: {str(e)}")
            raise ValueError(str(e))

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            data = dict(place_data or {})

            if 'title' in data:
                if len(data['title']) > 100:
                    raise ValueError("Title must be 100 characters or less")
                place.title = data['title']

            if 'description' in data:
                place.description = data['description']

            if 'price' in data:
                if float(data['price']) < 0:
                    raise ValueError("Price must be a non-negative number")
                place.price = float(data['price'])

            if 'latitude' in data:
                if not (-90 <= float(data['latitude']) <= 90):
                    raise ValueError("Latitude must be between -90 and 90")
                place.latitude = float(data['latitude'])

            if 'longitude' in data:
                if not (-180 <= float(data['longitude']) <= 180):
                    raise ValueError("Longitude must be between -180 and 180")
                place.longitude = float(data['longitude'])

            if 'owner_id' in data:
                owner = self.user_repo.get_by_id(data['owner_id'])  # ✅ fix: get_by_id
                if owner:
                    place.owner = owner
                else:
                    raise ValueError(f"User with id {data['owner_id']} not found")

            if 'amenities' in data:
                place.amenities = []  # reset
                for amenity_id in data['amenities']:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)

            logger.debug(f"Successfully updated place {place_id}")
            db.session.commit()
            return place

        except Exception as e:
            logger.error(f"Error updating place: {str(e)}")
            raise ValueError(str(e))

    def delete_place(self, place_id):
        """Supprime un place par son ID."""
        logger.debug(f"Attempting to delete place with ID: {place_id}")
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        self.place_repo.delete(place_id)
        logger.debug(f"Place {place_id} successfully deleted")
        return True

    # ----------------------------------------------------------------------
    # REVIEWS
    # ----------------------------------------------------------------------

    def create_review(self, review_data):
        if not (1 <= review_data.get('rating', 0) <= 5):
            raise ValueError("Rating must be between 1 and 5")
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")
        review = Review(
            text=review_data.get('text', ''),
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if review:
            if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5")
            self.review_repo.update(review_id, review_data)
            return review
        return None

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

    def has_already_reviewed(self, user_id, place_id):
        """Vérifie si un utilisateur a déjà commenté un lieu donné."""
        reviews = self.review_repo.get_all()
        for review in reviews:
            if str(review.user.id) == str(user_id) and str(review.place.id) == str(place_id):
                return True
        return False