#  HBNB API Testing Guide

##  Core Validations

### 1. User Model
- First/Last name: non-empty, ≤ 50 chars
- Email: valid format, unique
```python
def test_user_validation():
    # Valid user
    response = client.post('/api/v1/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 201

    # Invalid email
    response = client.post('/api/v1/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email"
    })
    assert response.status_code == 400
```

### 2. Place Model
- Title: non-empty, ≤ 100 chars
- Price: > 0
- Coordinates: lat (-90 to 90), long (-180 to 180)

### 3. Review Model
- Text: non-empty
- Rating: 1-5
- Valid user_id and place_id

##  API Testing

### User Endpoints
```bash
# Create User
curl -X POST "http://localhost:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com"
     }'

# Expected: 201 Created
{
    "id": "uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}
```

### Place Endpoints
```bash
# Create Place
curl -X POST "http://localhost:5000/api/v1/places/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Cozy Apartment",
         "price": 100.0,
         "latitude": 37.7749,
         "longitude": -122.4194,
         "owner_id": "user_uuid"
     }'

# Expected: 201 Created
```

### Common Error Cases
```bash
# Invalid Data (400 Bad Request)
curl -X POST "http://localhost:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "",
         "email": "invalid"
     }'

# Resource Not Found (404)
curl -X GET "http://localhost:5000/api/v1/places/invalid-id"
```

##  Test Coverage

### Essential Test Cases
1. **Creation Tests**
   - Valid data  201
   - Invalid data  400
   - Duplicate data  400

2. **Retrieval Tests**
   - Existing resource  200
   - Non-existent resource  404

3. **Update Tests**
   - Valid update  200
   - Invalid data  400
   - Non-existent resource  404

4. **Relationship Tests**
   - Place with owner details
   - Place with reviews
   - Place with amenities

##  Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_users.py
```

---
>  **Note**: Use the Swagger documentation at `http://localhost:5000/api/v1/` for interactive API testing.

---
##  Summary
This testing guide provides comprehensive validation rules, API endpoint tests, and coverage scenarios to ensure the HBNB application's reliability and proper functionality across all its components.
