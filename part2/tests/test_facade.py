"""
Unit tests for HBnBFacade (FACADE)
Tests orchestration between layers
"""
import unittest
from FACADE.facade import HBnBFacade
class TestHBnBFacade(unittest.TestCase):
    """Test cases for HBnBFacade"""
    def setUp(self):
        """Set up a fresh facade before each test"""
        self.facade = HBnBFacade()
    # ==================== USER TESTS ====================
    def test_create_user_success(self):
        """Test successful user creation"""
        data = {
            "email": "alice@test.com",
            "password": "secret123",
            "first_name": "Alice",
            "last_name": "Dupont"
        }
        user = self.facade.create_user(data)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "alice@test.com")
        self.assertEqual(user.first_name, "Alice")
    def test_create_user_duplicate_email(self):
        """Test that duplicate email raises error"""
        data = {
            "email": "alice@test.com",
            "password": "pass"
        }
        # Create first user
        self.facade.create_user(data)
        # Try to create duplicate
        with self.assertRaises(ValueError) as context:
            self.facade.create_user(data)
        self.assertIn("Email already exists", str(context.exception))
    def test_get_user_success(self):
        """Test retrieving an existing user"""
        data = {"email": "test@test.com", "password": "pass"}
        created = self.facade.create_user(data)
        retrieved = self.facade.get_user(created.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, created.id)
    def test_get_user_not_found(self):
        """Test getting non-existent user returns None"""
        result = self.facade.get_user("fake-uuid-123")
        self.assertIsNone(result)
    def test_update_user_success(self):
        """Test updating user"""
        data = {"email": "test@test.com", "password": "pass", "first_name": "John"}
        user = self.facade.create_user(data)
        update_data = {"first_name": "Jane"}
        updated = self.facade.update_user(user.id, update_data)
        self.assertEqual(updated.first_name, "Jane")
    def test_update_user_email_uniqueness(self):
        """Test that updating email checks for uniqueness"""
        user1 = self.facade.create_user({"email": "user1@test.com", "password": "pass"})
        user2 = self.facade.create_user({"email": "user2@test.com", "password": "pass"})
        # Try to update user2 with user1's email
        with self.assertRaises(ValueError) as context:
            self.facade.update_user(user2.id, {"email": "user1@test.com"})
        self.assertIn("Email already exists", str(context.exception))
    # ==================== AMENITY TESTS ====================
    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        data = {"name": "Wi-Fi"}
        amenity = self.facade.create_amenity(data)
        self.assertIsNotNone(amenity)
        self.assertEqual(amenity.name, "Wi-Fi")
    def test_get_all_amenities(self):
        """Test listing all amenities"""
        self.facade.create_amenity({"name": "Wi-Fi"})
        self.facade.create_amenity({"name": "Pool"})
        amenities = self.facade.get_all_amenities()
        self.assertEqual(len(amenities), 2)
    # ==================== PLACE TESTS ====================
    def test_create_place_success(self):
        """Test successful place creation"""
        # Create owner first
        user = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        place_data = {
            "name": "Beach House",
            "owner_id": user.id,
            "price": 100.0
        }
        place = self.facade.create_place(place_data)
        self.assertIsNotNone(place)
        self.assertEqual(place.name, "Beach House")
        self.assertEqual(place.owner_id, user.id)
    def test_create_place_invalid_owner(self):
        """Test that creating place with invalid owner fails"""
        place_data = {
            "name": "Test Place",
            "owner_id": "fake-owner-id"
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Owner not found", str(context.exception))
    def test_create_place_with_amenities(self):
        """Test creating place with amenities"""
        user = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        wifi = self.facade.create_amenity({"name": "Wi-Fi"})
        pool = self.facade.create_amenity({"name": "Pool"})
        place_data = {
            "name": "Luxury Villa",
            "owner_id": user.id,
            "amenity_ids": [wifi.id, pool.id]
        }
        place = self.facade.create_place(place_data)
        self.assertEqual(len(place.amenity_ids), 2)
        self.assertIn(wifi.id, place.amenity_ids)
        self.assertIn(pool.id, place.amenity_ids)
    def test_create_place_invalid_amenity(self):
        """Test that invalid amenity_id raises error"""
        user = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        place_data = {
            "name": "Test Place",
            "owner_id": user.id,
            "amenity_ids": ["fake-amenity-id"]
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Amenity", str(context.exception))
        self.assertIn("not found", str(context.exception))
    def test_serialize_place_extended(self):
        """Test extended serialization of place"""
        user = self.facade.create_user({
            "email": "owner@test.com",
            "password": "pass",
            "first_name": "Alice",
            "last_name": "Dupont"
        })
        wifi = self.facade.create_amenity({"name": "Wi-Fi"})
        place = self.facade.create_place({
            "name": "Chalet",
            "owner_id": user.id,
            "amenity_ids": [wifi.id]
        })
        serialized = self.facade.serialize_place_extended(place)
        # Check extended fields
        self.assertIn('owner_first_name', serialized)
        self.assertIn('owner_last_name', serialized)
        self.assertIn('amenities', serialized)
        self.assertEqual(serialized['owner_first_name'], "Alice")
        self.assertEqual(serialized['owner_last_name'], "Dupont")
        self.assertEqual(len(serialized['amenities']), 1)
        self.assertEqual(serialized['amenities'][0]['name'], "Wi-Fi")
    # ==================== REVIEW TESTS ====================
    def test_create_review_success(self):
        """Test successful review creation"""
        user = self.facade.create_user({"email": "user@test.com", "password": "pass"})
        owner = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        place = self.facade.create_place({"name": "Place", "owner_id": owner.id})
        review_data = {
            "text": "Great place!",
            "user_id": user.id,
            "place_id": place.id
        }
        review = self.facade.create_review(review_data)
        self.assertIsNotNone(review)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.user_id, user.id)
        self.assertEqual(review.place_id, place.id)
    def test_create_review_invalid_user(self):
        """Test that invalid user_id raises error"""
        owner = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        place = self.facade.create_place({"name": "Place", "owner_id": owner.id})
        review_data = {
            "text": "Great!",
            "user_id": "fake-user-id",
            "place_id": place.id
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("User not found", str(context.exception))
    def test_create_review_invalid_place(self):
        """Test that invalid place_id raises error"""
        user = self.facade.create_user({"email": "user@test.com", "password": "pass"})
        review_data = {
            "text": "Great!",
            "user_id": user.id,
            "place_id": "fake-place-id"
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("Place not found", str(context.exception))
    def test_get_reviews_by_place(self):
        """Test getting reviews for a place"""
        user = self.facade.create_user({"email": "user@test.com", "password": "pass"})
        owner = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        place = self.facade.create_place({"name": "Place", "owner_id": owner.id})
        review1 = self.facade.create_review({
            "text": "Great!",
            "user_id": user.id,
            "place_id": place.id
        })
        review2 = self.facade.create_review({
            "text": "Excellent!",
            "user_id": user.id,
            "place_id": place.id
        })
        reviews = self.facade.get_reviews_by_place(place.id)
        self.assertEqual(len(reviews), 2)
    def test_delete_review_success(self):
        """Test deleting a review"""
        user = self.facade.create_user({"email": "user@test.com", "password": "pass"})
        owner = self.facade.create_user({"email": "owner@test.com", "password": "pass"})
        place = self.facade.create_place({"name": "Place", "owner_id": owner.id})
        review = self.facade.create_review({
            "text": "Great!",
            "user_id": user.id,
            "place_id": place.id
        })
        result = self.facade.delete_review(review.id)
        self.assertTrue(result)
        # Verify deletion
        retrieved = self.facade.get_review(review.id)
        self.assertIsNone(retrieved)
    def test_delete_review_not_found(self):
        """Test deleting non-existent review raises error"""
        with self.assertRaises(ValueError) as context:
            self.facade.delete_review("fake-review-id")
        self.assertIn("Review not found", str(context.exception))
if __name__ == '__main__':
    unittest.main()
