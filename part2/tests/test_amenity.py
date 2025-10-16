"""
Unit tests for Amenity entity (BLL)
Tests business logic and validations
"""
import unittest
from BLL.amenity import Amenity
class TestAmenity(unittest.TestCase):
    """Test cases for Amenity entity"""
    def test_amenity_creation_valid(self):
        """Test creating an amenity with valid data"""
        amenity = Amenity(name="Wi-Fi")
        self.assertIsNotNone(amenity.id)
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)
    def test_amenity_name_required(self):
        """Test that name is required"""
        with self.assertRaises(ValueError) as context:
            Amenity(name="")
        self.assertIn("Amenity name is required", str(context.exception))
    def test_amenity_name_whitespace_only(self):
        """Test that name cannot be only whitespace"""
        with self.assertRaises(ValueError) as context:
            Amenity(name="   ")
        self.assertIn("Amenity name is required", str(context.exception))
    def test_amenity_name_strips_whitespace(self):
        """Test that name is stripped of whitespace"""
        amenity = Amenity(name="  Pool  ")
        self.assertEqual(amenity.name, "Pool")
    def test_amenity_to_dict(self):
        """Test to_dict() method"""
        amenity = Amenity(name="Parking")
        amenity_dict = amenity.to_dict()
        self.assertIn('id', amenity_dict)
        self.assertIn('name', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)
        self.assertEqual(amenity_dict['name'], "Parking")
    def test_amenity_multiple_instances(self):
        """Test creating multiple amenities"""
        amenity1 = Amenity(name="Wi-Fi")
        amenity2 = Amenity(name="Pool")
        # IDs should be different
        self.assertNotEqual(amenity1.id, amenity2.id)
        # Names should be preserved
        self.assertEqual(amenity1.name, "Wi-Fi")
        self.assertEqual(amenity2.name, "Pool")
if __name__ == '__main__':
    unittest.main()
