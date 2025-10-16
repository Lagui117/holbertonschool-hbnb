"""
Unit tests for InMemoryRepository (PL)
Tests data storage and retrieval operations
"""

import unittest
from PL.in_memory_repository import InMemoryRepository
from business.user import User
from business.amenity import Amenity
from business.place import Place
from business.review import Review
class TestInMemoryRepository(unittest.TestCase):
    """Test cases for InMemoryRepository"""
    def setUp(self):
        """Set up a fresh repository before each test"""
        self.repo = InMemoryRepository()
    # ==================== ADD TESTS ====================
    def test_add_user(self):
        """Test adding a user to repository"""
        user = User(email="test@test.com", password="pass")
        result = self.repo.add(user)
        self.assertEqual(result, user)
        self.assertEqual(result.id, user.id)
    def test_add_multiple_entities(self):
        """Test adding multiple different entities"""
        user = User(email="test@test.com", password="pass")
        amenity = Amenity(name="Wi-Fi")
        self.repo.add(user)
        self.repo.add(amenity)
        # Both should be stored
        retrieved_user = self.repo.get(User, user.id)
        retrieved_amenity = self.repo.get(Amenity, amenity.id)
        self.assertEqual(retrieved_user.id, user.id)
        self.assertEqual(retrieved_amenity.id, amenity.id)
    # ==================== GET TESTS ====================
    def test_get_existing_user(self):
        """Test retrieving an existing user"""
        user = User(email="test@test.com", password="pass")
        self.repo.add(user)
        retrieved = self.repo.get(User, user.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, user.id)
        self.assertEqual(retrieved.email, user.email)
    def test_get_nonexistent_user(self):
        """Test retrieving a non-existent user returns None"""
        result = self.repo.get(User, "fake-uuid-123")
        self.assertIsNone(result)
    def test_get_wrong_class(self):
        """Test getting with wrong class returns None"""
        user = User(email="test@test.com", password="pass")
        self.repo.add(user)
        # Try to get user as Amenity
        result = self.repo.get(Amenity, user.id)
        self.assertIsNone(result)
    # ==================== ALL TESTS ====================
    def test_all_empty(self):
        """Test getting all when repository is empty"""
        users = self.repo.all(User)
        self.assertEqual(users, [])
    def test_all_users(self):
        """Test getting all users"""
        user1 = User(email="user1@test.com", password="pass")
        user2 = User(email="user2@test.com", password="pass")
        self.repo.add(user1)
        self.repo.add(user2)
        users = self.repo.all(User)
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)
    def test_all_filters_by_class(self):
        """Test that all() only returns entities of specified class"""
        user = User(email="test@test.com", password="pass")
        amenity = Amenity(name="Wi-Fi")
        self.repo.add(user)
        self.repo.add(amenity)
        users = self.repo.all(User)
        amenities = self.repo.all(Amenity)
        self.assertEqual(len(users), 1)
        self.assertEqual(len(amenities), 1)
        self.assertIn(user, users)
        self.assertNotIn(amenity, users)
    # ==================== UPDATE TESTS ====================
    def test_update_user(self):
        """Test updating a user"""
        user = User(email="test@test.com", password="pass", first_name="John")
        self.repo.add(user)
        # Modify user
        user.first_name = "Jane"
        updated = self.repo.update(user)
        self.assertEqual(updated.first_name, "Jane")
        # Verify persistence
        retrieved = self.repo.get(User, user.id)
        self.assertEqual(retrieved.first_name, "Jane")
    def test_update_nonexistent_raises_error(self):
        """Test updating non-existent entity raises error"""
        user = User(email="test@test.com", password="pass")
        # Don't add to repo
        with self.assertRaises(ValueError):
            self.repo.update(user)
    # ==================== DELETE TESTS ====================
    def test_delete_user(self):
        """Test deleting a user"""
        user = User(email="test@test.com", password="pass")
        self.repo.add(user)
        result = self.repo.delete(user)
        self.assertTrue(result)
        # Verify deletion
        retrieved = self.repo.get(User, user.id)
        self.assertIsNone(retrieved)
    def test_delete_nonexistent_returns_false(self):
        """Test deleting non-existent entity returns False"""
        user = User(email="test@test.com", password="pass")
        # Don't add to repo
        result = self.repo.delete(user)
        self.assertFalse(result)
    # ==================== SPECIAL METHODS TESTS ====================
    def test_find_by_email_existing(self):
        """Test finding user by email"""
        user = User(email="test@test.com", password="pass")
        self.repo.add(user)
        found = self.repo.find_by_email("test@test.com")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, user.id)
    def test_find_by_email_case_insensitive(self):
        """Test email search is case-insensitive"""
        user = User(email="Test@TEST.com", password="pass")
        self.repo.add(user)
        found = self.repo.find_by_email("test@test.com")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, user.id)
    def test_find_by_email_nonexistent(self):
        """Test finding non-existent email returns None"""
        result = self.repo.find_by_email("nonexistent@test.com")
        self.assertIsNone(result)
    def test_get_reviews_by_place(self):
        """Test getting reviews for a specific place"""
        place = Place(name="Test Place", owner_id="owner-123")
        self.repo.add(place)
        review1 = Review(text="Great!", user_id="user-1", place_id=place.id)
        review2 = Review(text="Good!", user_id="user-2", place_id=place.id)
        review3 = Review(text="Nice!", user_id="user-3", place_id="other-place-id")
        self.repo.add(review1)
        self.repo.add(review2)
        self.repo.add(review3)
        reviews = self.repo.get_reviews_by_place(place.id)
        self.assertEqual(len(reviews), 2)
        self.assertIn(review1, reviews)
        self.assertIn(review2, reviews)
        self.assertNotIn(review3, reviews)
if __name__ == '__main__':
    unittest.main()
