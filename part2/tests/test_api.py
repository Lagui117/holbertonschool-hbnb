"""
Integration tests for API endpoints
Tests HTTP requests and responses
"""
import unittest
import json
from app import app
class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints"""
    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
    # ==================== USER ENDPOINTS ====================
    def test_create_user_success(self):
        """Test POST /api/v1/users/ with valid data"""
        data = {
            "email": "alice@test.com",
            "password": "secret123",
            "first_name": "Alice",
            "last_name": "Dupont"
        }
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        json_data = json.loads(response.data)
        self.assertIn('id', json_data)
        self.assertEqual(json_data['email'], 'alice@test.com')
        self.assertNotIn('password', json_data)  # Password should NOT be in response
    def test_create_user_duplicate_email(self):
        """Test POST /api/v1/users/ with duplicate email"""
        data = {"email": "duplicate@test.com", "password": "pass"}
        # Create first user
        self.client.post('/api/v1/users/', data=json.dumps(data), content_type='application/json')
        # Try to create duplicate
        response = self.client.post('/api/v1/users/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertIn('error', json_data)
    def test_create_user_invalid_email(self):
        """Test POST /api/v1/users/ with invalid email format"""
        data = {"email": "invalid-email", "password": "pass"}
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    def test_get_users_list(self):
        """Test GET /api/v1/users/"""
        # Create some users
        self.client.post('/api/v1/users/',
                        data=json.dumps({"email": "user1@test.com", "password": "pass"}),
                        content_type='application/json')
        self.client.post('/api/v1/users/',
                        data=json.dumps({"email": "user2@test.com", "password": "pass"}),
                        content_type='application/json')
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)
        self.assertGreaterEqual(len(json_data), 2)
    def test_get_user_by_id(self):
        """Test GET /api/v1/users/<id>"""
        # Create a user
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "test@test.com", "password": "pass"}),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['id'], user_id)
    def test_get_user_not_found(self):
        """Test GET /api/v1/users/<id> with invalid ID"""
        response = self.client.get('/api/v1/users/fake-uuid-123')
        self.assertEqual(response.status_code, 404)
    def test_update_user(self):
        """Test PUT /api/v1/users/<id>"""
        # Create a user
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "test@test.com", "password": "pass", "first_name": "John"}),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        # Update the user
        update_data = {"first_name": "Jane"}
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['first_name'], 'Jane')
    # ==================== AMENITY ENDPOINTS ====================
    def test_create_amenity_success(self):
        """Test POST /api/v1/amenities/"""
        data = {"name": "Wi-Fi"}
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['name'], 'Wi-Fi')
    def test_get_amenities_list(self):
        """Test GET /api/v1/amenities/"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)
    # ==================== PLACE ENDPOINTS ====================
    def test_create_place_success(self):
        """Test POST /api/v1/places/"""
        # Create owner
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "owner@test.com", "password": "pass"}),
            content_type='application/json'
        )
        owner_id = json.loads(user_response.data)['id']
        # Create place
        place_data = {
            "name": "Beach House",
            "owner_id": owner_id,
            "price": 100.0
        }
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['name'], 'Beach House')
        # Check extended serialization
        self.assertIn('owner_first_name', json_data)
        self.assertIn('amenities', json_data)
    def test_create_place_invalid_owner(self):
        """Test POST /api/v1/places/ with invalid owner"""
        place_data = {
            "name": "Test Place",
            "owner_id": "fake-owner-id"
        }
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    def test_create_place_negative_price(self):
        """Test POST /api/v1/places/ with negative price"""
        # Create owner
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "owner@test.com", "password": "pass"}),
            content_type='application/json'
        )
        owner_id = json.loads(user_response.data)['id']
        place_data = {
            "name": "Test",
            "owner_id": owner_id,
            "price": -50
        }
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    def test_get_place_reviews(self):
        """Test GET /api/v1/places/<id>/reviews"""
        # Create owner and place
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "owner@test.com", "password": "pass"}),
            content_type='application/json'
        )
        owner_id = json.loads(user_response.data)['id']
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({"name": "Place", "owner_id": owner_id}),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        # Get reviews (should be empty initially)
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)
    # ==================== REVIEW ENDPOINTS ====================
    def test_create_review_success(self):
        """Test POST /api/v1/reviews/"""
        # Create user and place
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "user@test.com", "password": "pass"}),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "owner@test.com", "password": "pass"}),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({"name": "Place", "owner_id": owner_id}),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        # Create review
        review_data = {
            "text": "Great place!",
            "user_id": user_id,
            "place_id": place_id
        }
        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['text'], 'Great place!')
    def test_delete_review(self):
        """Test DELETE /api/v1/reviews/<id>"""
        # Create user and place
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "user@test.com", "password": "pass"}),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({"email": "owner@test.com", "password": "pass"}),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({"name": "Place", "owner_id": owner_id}),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        # Create review
        review_response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps({"text": "Great!", "user_id": user_id, "place_id": place_id}),
            content_type='application/json'
        )
        review_id = json.loads(review_response.data)['id']
        # Delete review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 204)
        # Verify deletion
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)
if __name__ == '__main__':
    unittest.main()
