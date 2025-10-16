"""
Unit tests for Place entity (BLL)
Tests business logic and validations
"""
import unittest
from business.place import Place
class TestPlace(unittest.TestCase):
    """Test cases for Place entity"""
    def test_place_creation_valid(self):
        """Test creating a place with valid data"""
        place = Place(
            name="Beach House",
            owner_id="owner-uuid-123",
            price=100.0,
            description="Beautiful beach house",
            latitude=45.5,
            longitude=-73.6
        )
        self.assertIsNotNone(place.id)
        self.assertEqual(place.name, "Beach House")
        self.assertEqual(place.owner_id, "owner-uuid-123")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 45.5)
        self.assertEqual(place.longitude, -73.6)
    def test_place_name_required(self):
        """Test that name is required"""
        with self.assertRaises(ValueError) as context:
            Place(name="", owner_id="owner-123")
        self.assertIn("Place name is required", str(context.exception))
    def test_place_owner_id_required(self):
        """Test that owner_id is required"""
        with self.assertRaises(ValueError) as context:
            Place(name="Test Place", owner_id="")
        self.assertIn("Owner ID is required", str(context.exception))
    def test_place_price_non_negative(self):
        """Test that price must be >= 0"""
        with self.assertRaises(ValueError) as context:
            Place(name="Test", owner_id="owner-123", price=-50)
        self.assertIn("Price must be >= 0", str(context.exception))
    def test_place_latitude_validation(self):
        """Test latitude must be between -90 and 90"""
        # Test latitude too high
        with self.assertRaises(ValueError) as context:
            Place(name="Test", owner_id="owner-123", latitude=100)
        self.assertIn("Latitude must be between -90 and 90", str(context.exception))
        # Test latitude too low
        with self.assertRaises(ValueError) as context:
            Place(name="Test", owner_id="owner-123", latitude=-100)
        self.assertIn("Latitude must be between -90 and 90", str(context.exception))
    def test_place_longitude_validation(self):
        """Test longitude must be between -180 and 180"""
        # Test longitude too high
        with self.assertRaises(ValueError) as context:
            Place(name="Test", owner_id="owner-123", longitude=200)
        self.assertIn("Longitude must be between -180 and 180", str(context.exception))
        # Test longitude too low
        with self.assertRaises(ValueError) as context:
            Place(name="Test", owner_id="owner-123", longitude=-200)
        self.assertIn("Longitude must be between -180 and 180", str(context.exception))
    def test_place_valid_coordinates(self):
        """Test valid coordinates are accepted"""
        place = Place(
            name="Test",
            owner_id="owner-123",
            latitude=45.5,
            longitude=-73.6
        )
        self.assertEqual(place.latitude, 45.5)
        self.assertEqual(place.longitude, -73.6)
    def test_place_optional_coordinates(self):
        """Test that coordinates are optional"""
        place = Place(
            name="Test",
            owner_id="owner-123"
        )
        self.assertIsNone(place.latitude)
        self.assertIsNone(place.longitude)
    def test_place_amenity_ids(self):
        """Test amenity_ids handling"""
        amenity_ids = ["amenity-1", "amenity-2"]
        place = Place(
            name="Test",
            owner_id="owner-123",
            amenity_ids=amenity_ids
        )
        self.assertEqual(place.amenity_ids, amenity_ids)
    def test_place_default_values(self):
        """Test default values"""
        place = Place(name="Test", owner_id="owner-123")
        self.assertEqual(place.price, 0.0)
        self.assertEqual(place.description, "")
        self.assertEqual(place.amenity_ids, [])
        self.assertEqual(place.reviews, [])
if __name__ == '__main__':
    unittest.main()
