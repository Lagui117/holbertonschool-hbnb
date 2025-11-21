import unittest
from app.models.place import Place
from app.models.user import User

class TestPlace(unittest.TestCase):
 #ef setUp(self):
 #elf.owner = User(first_name="John", last_name="Doe", email="john.doe@example.com")

 #ef test_valid_place(self):
 #lace = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=self.owner)
 #elf.assertEqual(place.title, "Cozy Apartment")
 #elf.assertEqual(place.price, 100)
 #elf.assertEqual(place.latitude, 37.7749)
 #elf.assertEqual(place.longitude, -122.4194)

 #ef test_invalid_title(self):
 #ith self.assertRaises(ValueError):
 #lace(title="", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=self.owner)

 #ef test_invalid_price(self):
 #ith self.assertRaises(ValueError):
 #lace(title="Cozy Apartment", description="A nice place to stay", price=-100, latitude=37.7749, longitude=-122.4194, owner=self.owner)

 #ef test_invalid_latitude(self):
 #ith self.assertRaises(ValueError):
 #lace(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=100, longitude=-122.4194, owner=self.owner)

 #ef test_invalid_longitude(self):
 #ith self.assertRaises(ValueError):
 #lace(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-200, owner=self.owner)

if __name__ == '__main__':
 #nittest.main()