import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class TestReview(unittest.TestCase):
 #ef setUp(self):
 #elf.user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
 #elf.place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=self.user)

 #ef test_valid_review(self):
 #eview = Review(text="Great place!", rating=5, place=self.place, user=self.user)
 #elf.assertEqual(review.text, "Great place!")
 #elf.assertEqual(review.rating, 5)

 #ef test_invalid_text(self):
 #ith self.assertRaises(ValueError):
 #eview(text="", rating=5, place=self.place, user=self.user)

 #ef test_invalid_rating(self):
 #ith self.assertRaises(ValueError):
 #eview(text="Great place!", rating=6, place=self.place, user=self.user)

 #ef test_invalid_place(self):
 #ith self.assertRaises(ValueError):
 #eview(text="Great place!", rating=5, place=None, user=self.user)

 #ef test_invalid_user(self):
 #ith self.assertRaises(ValueError):
 #eview(text="Great place!", rating=5, place=self.place, user=None)

if __name__ == '__main__':
 #nittest.main()