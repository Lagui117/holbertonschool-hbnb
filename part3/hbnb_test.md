  HBNB API Testing Guide

  Core Validations

 . User Model
- First/Last name: non-empty, ≤  chars
- Email: valid format, unique
```python
def test_user_validation():
     Valid user
    response = client.post('/api/v/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 

     Invalid email
    response = client.post('/api/v/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email"
    })
    assert response.status_code == 
```

 . Place Model
- Title: non-empty, ≤  chars
- Price: > 
- Coordinates: lat (- to ), long (- to )

 . Review Model
- Text: non-empty
- Rating: -
- Valid user_id and place_id

  API Testing

 User Endpoints
```bash
 Create User
curl -X POST "http://localhost:/api/v/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "John",
         "last_name": "Doe",
         "email": "john@example.com"
     }'

 Expected:  Created
{
    "id": "uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}
```

 Place Endpoints
```bash
 Create Place
curl -X POST "http://localhost:/api/v/places/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Cozy Apartment",
         "price": .,
         "latitude": .,
         "longitude": -.,
         "owner_id": "user_uuid"
     }'

 Expected:  Created
```

 Common Error Cases
```bash
 Invalid Data ( Bad Request)
curl -X POST "http://localhost:/api/v/users/" \
     -H "Content-Type: application/json" \
     -d '{
         "first_name": "",
         "email": "invalid"
     }'

 Resource Not Found ()
curl -X GET "http://localhost:/api/v/places/invalid-id"
```

  Test Coverage

 Essential Test Cases
. Creation Tests
   - Valid data  
   - Invalid data  
   - Duplicate data  

. Retrieval Tests
   - Existing resource  
   - Non-existent resource  

. Update Tests
   - Valid update  
   - Invalid data  
   - Non-existent resource  

. Relationship Tests
   - Place with owner details
   - Place with reviews
   - Place with amenities

  Running Tests
```bash
 Run all tests
python -m pytest tests/

 Run specific test file
python -m pytest tests/test_users.py
```

---
>  Note: Use the Swagger documentation at `http://localhost:/api/v/` for interactive API testing.

---
  Summary
This testing guide provides comprehensive validation rules, API endpoint tests, and coverage scenarios to ensure the HBNB application's reliability and proper functionality across all its components.
