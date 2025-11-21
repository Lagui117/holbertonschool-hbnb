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
 #REEN = '\033[92m'
 #ED = '\033[91m'
 #ELLOW = '\033[93m'
 #LUE = '\033[94m'
 #ND = '\033[0m'

def print_success(msg):
 #rint(f"{Colors.GREEN} {msg}{Colors.END}")

def print_error(msg):
 #rint(f"{Colors.RED} {msg}{Colors.END}")

def print_info(msg):
 #rint(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_section(msg):
 #rint(f"\n{Colors.YELLOW}{'='*60}")
 #rint(f"  {msg}")
 #rint(f"{'='*60}{Colors.END}\n")

def test_login(email, password):
 #""Test login and return token"""
 #ry:
 #esponse = requests.post(
 #"{BASE_URL}/auth/login",
 #son={"email": email, "password": password}
 #
 #f response.status_code == 200:
 #oken = response.json().get('access_token')
 #rint_success(f"Login successful for {email}")
 #eturn token
 #lse:
 #rint_error(f"Login failed: {response.text}")
 #eturn None
 #xcept Exception as e:
 #rint_error(f"Login error: {str(e)}")
 #eturn None

def test_create_user(token=None):
 #""Test user creation"""
 #mport time
 #imestamp = int(time.time() * 1000)
 #ata = {
 #first_name": "Test",
 #last_name": "User",
 #email": f"test{timestamp}@example.com",
 #password": "test123"
 #
    
 #eaders = {}
 #f token:
 #eaders["Authorization"] = f"Bearer {token}"
    
 #ry:
 #esponse = requests.post(
 #"{BASE_URL}/users/",
 #son=data,
 #eaders=headers
 #
 #f response.status_code == 201:
 #ser_id = response.json().get('id')
 #rint_success(f"User created successfully (ID: {user_id})")
 #eturn user_id, data
 #lse:
 #rint_error(f"User creation failed: {response.text}")
 #eturn None, None
 #xcept Exception as e:
 #rint_error(f"User creation error: {str(e)}")
 #eturn None, None

def test_create_amenity(token):
 #""Test amenity creation (admin only)"""
 #mport time
 #imestamp = int(time.time() * 1000)
 #ata = {"name": f"TestAmenity{timestamp}"}
    
 #ry:
 #esponse = requests.post(
 #"{BASE_URL}/amenities/",
 #son=data,
 #eaders={"Authorization": f"Bearer {token}"}
 #
 #f response.status_code == 201:
 #menity_id = response.json().get('id')
 #rint_success(f"Amenity created successfully (ID: {amenity_id})")
 #eturn amenity_id
 #lse:
 #rint_error(f"Amenity creation failed: {response.text}")
 #eturn None
 #xcept Exception as e:
 #rint_error(f"Amenity creation error: {str(e)}")
 #eturn None

def test_create_place(token, amenity_ids):
 #""Test place creation"""
 #ata = {
 #title": "Test Place",
 #description": "A beautiful test place",
 #price": 100.0,
 #latitude": 45.5,
 #longitude": -73.6,
 #amenities": amenity_ids
 #
    
 #ry:
 #esponse = requests.post(
 #"{BASE_URL}/places/",
 #son=data,
 #eaders={"Authorization": f"Bearer {token}"}
 #
 #f response.status_code == 201:
 #lace_id = response.json().get('id')
 #rint_success(f"Place created successfully (ID: {place_id})")
 #eturn place_id
 #lse:
 #rint_error(f"Place creation failed: {response.text}")
 #eturn None
 #xcept Exception as e:
 #rint_error(f"Place creation error: {str(e)}")
 #eturn None

def test_create_review(token, place_id):
 #""Test review creation"""
 #ata = {
 #text": "Great place!",
 #rating": 5,
 #place_id": str(place_id)
 #
    
 #ry:
 #esponse = requests.post(
 #"{BASE_URL}/reviews/",
 #son=data,
 #eaders={"Authorization": f"Bearer {token}"}
 #
 #f response.status_code == 201:
 #eview_id = response.json().get('id')
 #rint_success(f"Review created successfully (ID: {review_id})")
 #eturn review_id
 #lse:
 #rint_error(f"Review creation failed: {response.text}")
 #eturn None
 #xcept Exception as e:
 #rint_error(f"Review creation error: {str(e)}")
 #eturn None

def test_get_places():
 #""Test getting all places (public)"""
 #ry:
 #esponse = requests.get(f"{BASE_URL}/places/")
 #f response.status_code == 200:
 #laces = response.json()
 #rint_success(f"Retrieved {len(places)} places")
 #eturn True
 #lse:
 #rint_error(f"Get places failed: {response.text}")
 #eturn False
 #xcept Exception as e:
 #rint_error(f"Get places error: {str(e)}")
 #eturn False

def test_admin_only_access(token):
 #""Test that non-admin cannot access admin endpoints"""
 #ry:
 #esponse = requests.get(
 #"{BASE_URL}/users/",
 #eaders={"Authorization": f"Bearer {token}"}
 #
 #f response.status_code == 403:
 #rint_success("Admin-only endpoint correctly blocked for non-admin")
 #eturn True
 #lse:
 #rint_error(f"Non-admin accessed admin endpoint: {response.text}")
 #eturn False
 #xcept Exception as e:
 #rint_error(f"Admin access test error: {str(e)}")
 #eturn False

def main():
 #""Main test function"""
 #rint_section("HBnB Part 3 - API Validation Tests")
    
    # Test 1: Admin Login
 #rint_section("Test 1: Admin Login")
 #dmin_token = test_login("admin@hbnb.io", "admin1234")
 #f not admin_token:
 #rint_error("Admin login failed. Make sure to run create_first_admin.py first!")
 #ys.exit(1)
    
    # Test 2: Create Standard User
 #rint_section("Test 2: Create Standard User (Public)")
 #ser_id, user_data = test_create_user()
 #f not user_id:
 #rint_error("User creation failed")
 #eturn
    
    # Test 3: User Login
 #rint_section("Test 3: User Login")
 #ser_token = test_login(user_data["email"], user_data["password"])
 #f not user_token:
 #rint_error("User login failed")
 #eturn
    
    # Test 4: Non-admin cannot access admin endpoints
 #rint_section("Test 4: Authorization Check (Non-admin)")
 #est_admin_only_access(user_token)
    
    # Test 5: Create Amenities (Admin)
 #rint_section("Test 5: Create Amenities (Admin Only)")
 #menity_id = test_create_amenity(admin_token)
 #f not amenity_id:
 #rint_error("Amenity creation failed")
 #eturn
    
    # Test 6: Create Place (Authenticated User)
 #rint_section("Test 6: Create Place (Authenticated User)")
 #lace_id = test_create_place(user_token, [amenity_id])
 #f not place_id:
 #rint_error("Place creation failed")
 #eturn
    
    # Test 7: Get All Places (Public)
 #rint_section("Test 7: Get All Places (Public)")
 #est_get_places()
    
    # Test 8: Create Second User for Review
 #rint_section("Test 8: Create Second User")
 #ser2_id, user2_data = test_create_user()
 #f not user2_id:
 #rint_error("Second user creation failed")
 #eturn
    
 #ser2_token = test_login(user2_data["email"], user2_data["password"])
 #f not user2_token:
 #rint_error("Second user login failed")
 #eturn
    
    # Test 9: Create Review (Different User)
 #rint_section("Test 9: Create Review (Different User)")
 #eview_id = test_create_review(user2_token, place_id)
    
    # Final Summary
 #rint_section("Test Summary")
 #rint_success("All critical tests completed!")
 #rint_info("Check the results above for any errors")
 #rint_info("\nFor manual testing, use the API_TESTING.md guide")

if __name__ == "__main__":
 #ry:
 #ain()
 #xcept KeyboardInterrupt:
 #rint("\n\nTests interrupted by user")
 #ys.exit(0)
 #xcept Exception as e:
 #rint_error(f"Unexpected error: {str(e)}")
 #ys.exit(1)
