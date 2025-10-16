"""
Unit tests for Review entity (BLL)
Tests business logic and validations
"""
import unittest
from business.review import Review
class TestReview(unittest.TestCase):
    """Test cases for Review entity"""
    def test_review_creation_valid(self):
        """Test creating a review with valid data"""
        review = Review(
            text="Great place!",
            user_id="user-uuid-123",
            place_id="place-uuid-456"
        )
        self.assertIsNotNone(review.id)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.user_id, "user-uuid-123")
        self.assertEqual(review.place_id, "place-uuid-456")
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)
    def test_review_text_required(self):
        """Test that text is required"""
        with self.assertRaises(ValueError) as context:
            Review(
                text="",
                user_id="user-123",
                place_id="place-123"
            )
        self.assertIn("Review text cannot be empty", str(context.exception))
    def test_review_text_whitespace_only(self):
        """Test that text cannot be only whitespace"""
        with self.assertRaises(ValueError) as context:
            Review(
                text="   ",
                user_id="user-123",
                place_id="place-123"
            )
        self.assertIn("Review text cannot be empty", str(context.exception))
    def test_review_user_id_required(self):
        """Test that user_id is required"""
        with self.assertRaises(ValueError) as context:
            Review(
                text="Great!",
                user_id="",
                place_id="place-123"
            )
        self.assertIn("User ID is required", str(context.exception))
    def test_review_place_id_required(self):
        """Test that place_id is required"""
        with self.assertRaises(ValueError) as context:
            Review(
                text="Great!",
                user_id="user-123",
                place_id=""
            )
        self.assertIn("Place ID is required", str(context.exception))
    def test_review_text_strips_whitespace(self):
        """Test that text is stripped of leading/trailing whitespace"""
        review = Review(
            text="  Great place!  ",
            user_id="user-123",
            place_id="place-123"
        )
        self.assertEqual(review.text, "Great place!")
    def test_review_to_dict(self):
        """Test to_dict() method"""
        review = Review(
            text="Excellent!",
            user_id="user-123",
            place_id="place-456"
        )
        review_dict = review.to_dict()
        self.assertIn('id', review_dict)
        self.assertIn('text', review_dict)
        self.assertIn('user_id', review_dict)
        self.assertIn('place_id', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)
        self.assertEqual(review_dict['text'], "Excellent!")
        self.assertEqual(review_dict['user_id'], "user-123")
        self.assertEqual(review_dict['place_id'], "place-456")
if __name__ == '__main__':
    unittest.main()
