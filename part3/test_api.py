#!/usr/bin/env python3
"""
Script de validation complète de l'API HBnB Part 3
Complete validation script for HBnB Part 3 API

Ce script teste toutes les fonctionnalités principales de l'API
This script tests all main API functionalities
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_section(msg):
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}{Colors.END}\n")

def test_login(email, password):
    """Test login and return token"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            token = response.json().get('access_token')
            print_success(f"Login successful for {email}")
            return token
        else:
            print_error(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None

def test_create_user(token=None):
    """Test user creation"""
    import time
    timestamp = int(time.time() * 1000)
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test{timestamp}@example.com",
        "password": "test123"
    }
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/",
            json=data,
            headers=headers
        )
        if response.status_code == 201:
            user_id = response.json().get('id')
            print_success(f"User created successfully (ID: {user_id})")
            return user_id, data
        else:
            print_error(f"User creation failed: {response.text}")
            return None, None
    except Exception as e:
        print_error(f"User creation error: {str(e)}")
        return None, None

def test_create_amenity(token):
    """Test amenity creation (admin only)"""
    import time
    timestamp = int(time.time() * 1000)
    data = {"name": f"TestAmenity{timestamp}"}
    
    try:
        response = requests.post(
            f"{BASE_URL}/amenities/",
            json=data,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 201:
            amenity_id = response.json().get('id')
            print_success(f"Amenity created successfully (ID: {amenity_id})")
            return amenity_id
        else:
            print_error(f"Amenity creation failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Amenity creation error: {str(e)}")
        return None

def test_create_place(token, amenity_ids):
    """Test place creation"""
    data = {
        "title": "Test Place",
        "description": "A beautiful test place",
        "price": 100.0,
        "latitude": 45.5,
        "longitude": -73.6,
        "amenities": amenity_ids
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/places/",
            json=data,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 201:
            place_id = response.json().get('id')
            print_success(f"Place created successfully (ID: {place_id})")
            return place_id
        else:
            print_error(f"Place creation failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Place creation error: {str(e)}")
        return None

def test_create_review(token, place_id):
    """Test review creation"""
    data = {
        "text": "Great place!",
        "rating": 5,
        "place_id": str(place_id)
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/reviews/",
            json=data,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 201:
            review_id = response.json().get('id')
            print_success(f"Review created successfully (ID: {review_id})")
            return review_id
        else:
            print_error(f"Review creation failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Review creation error: {str(e)}")
        return None

def test_get_places():
    """Test getting all places (public)"""
    try:
        response = requests.get(f"{BASE_URL}/places/")
        if response.status_code == 200:
            places = response.json()
            print_success(f"Retrieved {len(places)} places")
            return True
        else:
            print_error(f"Get places failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Get places error: {str(e)}")
        return False

def test_admin_only_access(token):
    """Test that non-admin cannot access admin endpoints"""
    try:
        response = requests.get(
            f"{BASE_URL}/users/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 403:
            print_success("Admin-only endpoint correctly blocked for non-admin")
            return True
        else:
            print_error(f"Non-admin accessed admin endpoint: {response.text}")
            return False
    except Exception as e:
        print_error(f"Admin access test error: {str(e)}")
        return False

def main():
    """Main test function"""
    print_section("HBnB Part 3 - API Validation Tests")
    
    # Test 1: Admin Login
    print_section("Test 1: Admin Login")
    admin_token = test_login("admin@hbnb.io", "admin1234")
    if not admin_token:
        print_error("Admin login failed. Make sure to run create_first_admin.py first!")
        sys.exit(1)
    
    # Test 2: Create Standard User
    print_section("Test 2: Create Standard User (Public)")
    user_id, user_data = test_create_user()
    if not user_id:
        print_error("User creation failed")
        return
    
    # Test 3: User Login
    print_section("Test 3: User Login")
    user_token = test_login(user_data["email"], user_data["password"])
    if not user_token:
        print_error("User login failed")
        return
    
    # Test 4: Non-admin cannot access admin endpoints
    print_section("Test 4: Authorization Check (Non-admin)")
    test_admin_only_access(user_token)
    
    # Test 5: Create Amenities (Admin)
    print_section("Test 5: Create Amenities (Admin Only)")
    amenity_id = test_create_amenity(admin_token)
    if not amenity_id:
        print_error("Amenity creation failed")
        return
    
    # Test 6: Create Place (Authenticated User)
    print_section("Test 6: Create Place (Authenticated User)")
    place_id = test_create_place(user_token, [amenity_id])
    if not place_id:
        print_error("Place creation failed")
        return
    
    # Test 7: Get All Places (Public)
    print_section("Test 7: Get All Places (Public)")
    test_get_places()
    
    # Test 8: Create Second User for Review
    print_section("Test 8: Create Second User")
    user2_id, user2_data = test_create_user()
    if not user2_id:
        print_error("Second user creation failed")
        return
    
    user2_token = test_login(user2_data["email"], user2_data["password"])
    if not user2_token:
        print_error("Second user login failed")
        return
    
    # Test 9: Create Review (Different User)
    print_section("Test 9: Create Review (Different User)")
    review_id = test_create_review(user2_token, place_id)
    
    # Final Summary
    print_section("Test Summary")
    print_success("All critical tests completed!")
    print_info("Check the results above for any errors")
    print_info("\nFor manual testing, use the API_TESTING.md guide")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
