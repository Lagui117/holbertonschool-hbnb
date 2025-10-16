"""
Unit tests for User entity (BLL)
Tests business logic and validations
"""
import unittest
from BLL.user import User
class TestUser(unittest.TestCase):
    """Test cases for User entity"""
    def test_user_creation_valid(self):
        """Test creating a user with valid data"""
        user = User(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
    def test_user_email_required(self):
        """Test that email is required"""
        with self.assertRaises(ValueError) as context:
            User(email="", password="password123")
        self.assertIn("Email is required", str(context.exception))
    def test_user_email_format_validation(self):
        """Test that email must contain @"""
        with self.assertRaises(ValueError) as context:
            User(email="invalidemail", password="password123")
        self.assertIn("Invalid email format", str(context.exception))
    def test_user_password_required(self):
        """Test that password is required"""
        with self.assertRaises(ValueError) as context:
            User(email="test@example.com", password="")
        self.assertIn("Password is required", str(context.exception))
    def test_user_email_lowercase(self):
        """Test that email is converted to lowercase"""
        user = User(
            email="TEST@EXAMPLE.COM",
            password="password123"
        )
        self.assertEqual(user.email, "test@example.com")
    def test_user_to_dict_excludes_password(self):
        """Test that to_dict() does not include password"""
        user = User(
            email="test@example.com",
            password="secret123",
            first_name="John"
        )
        user_dict = user.to_dict()
        self.assertNotIn('password', user_dict)
        self.assertIn('email', user_dict)
        self.assertIn('first_name', user_dict)
        self.assertIn('id', user_dict)
    def test_user_optional_names(self):
        """Test that first_name and last_name are optional"""
        user = User(
            email="test@example.com",
            password="password123"
        )
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
if __name__ == '__main__':
    unittest.main()
