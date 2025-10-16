# HBnB Project - Part 2: RESTful API Implementation
# Projet HBnB - Partie 2 : Implémentation de l'API RESTful

---

## 📋 Table of Contents / Table des matières

**English:**
1. [Project Overview](#project-overview-english)
2. [Architecture](#architecture-english)
3. [Project Structure](#project-structure-english)
4. [Installation & Setup](#installation--setup-english)
5. [API Endpoints](#api-endpoints-english)
6. [Business Logic & Validations](#business-logic--validations-english)
7. [Testing with cURL](#testing-with-curl-english)
8. [Code Examples](#code-examples-english)
9. [Design Patterns](#design-patterns-english)
10. [Next Steps (Part 3)](#next-steps-part-3-english)

**Français:**
1. [Vue d'ensemble du projet](#vue-densemble-du-projet-français)
2. [Architecture](#architecture-français)
3. [Structure du projet](#structure-du-projet-français)
4. [Installation & Configuration](#installation--configuration-français)
5. [Points de terminaison API](#points-de-terminaison-api-français)
6. [Logique métier & Validations](#logique-métier--validations-français)
7. [Tests avec cURL](#tests-avec-curl-français)
8. [Exemples de code](#exemples-de-code-français)
9. [Patrons de conception](#patrons-de-conception-français)
10. [Prochaines étapes (Partie 3)](#prochaines-étapes-partie-3-français)

---

# ENGLISH VERSION

## Project Overview (English)

### What is HBnB?

HBnB is a simplified **Airbnb-like application** designed to manage:
- **Users** (property owners and reviewers)
- **Places** (accommodations/listings)
- **Amenities** (facilities like Wi-Fi, Pool, Parking)
- **Reviews** (user feedback on places)

### Part 2 Goals

In **Part 2**, we implement:
1. ✅ **Business Logic Layer** (entities: User, Place, Review, Amenity)
2. ✅ **Persistence Layer** (in-memory repository)
3. ✅ **Presentation Layer** (RESTful API with Flask)
4. ✅ **Facade Pattern** (orchestration between layers)
5. ✅ **Complete CRUD operations** (Create, Read, Update, Delete)
6. ✅ **Data validations** (email uniqueness, price constraints, coordinates, etc.)

**Why Flask Pure (without Flask-RESTX)?**
- **Simplicity**: Single dependency (Flask only)
- **Control**: Full control over routes and responses
- **Learning**: Understand REST fundamentals
- **Testability**: Easy to test with cURL

---

## Architecture (English)

### 3-Layer Architecture

```
┌─────────────────────────────────────────┐
│   PRESENTATION LAYER (API)              │
│   - Flask Blueprints                    │
│   - HTTP endpoints                      │
│   - JSON serialization                  │
│   - Error handling (400, 404, etc.)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   BUSINESS LOGIC LAYER (Facade)         │
│   - HBnBFacade (orchestration)          │
│   - Input validation                    │
│   - Business rules enforcement          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   DOMAIN LAYER (Entities)               │
│   - User, Place, Review, Amenity        │
│   - BaseModel (UUID + timestamps)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   PERSISTENCE LAYER (Repository)        │
│   - InMemoryRepository                  │
│   - CRUD operations                     │
│   - (Will become SQLAlchemy in Part 3)  │
└─────────────────────────────────────────┘
```

### Why This Architecture?

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Maintainability**: Easy to modify one layer without affecting others
3. **Testability**: Each layer can be tested independently
4. **Scalability**: Easy to add new features or swap implementations
5. **Clean Code**: Clear dependencies and data flow

---

## Project Structure (English)

```
part2/
│
├── 📄 app.py                              # Flask application entry point
├── 📄 requirements.txt                    # Python dependencies (Flask only)
├── 📄 README.md                          # This file (EN/FR)
├── 📄 TESTING_GUIDE.md                   # Complete cURL testing guide
├── 📄 QUICKSTART.md                      # Quick start guide
│
├── 📂 api/                               # PRESENTATION LAYER
│   ├── __init__.py
│   ├── users.py                          # User endpoints (POST, GET, PUT)
│   ├── amenities.py                      # Amenity endpoints (POST, GET, PUT)
│   ├── places.py                         # Place endpoints (POST, GET, PUT, GET reviews)
│   └── reviews.py                        # Review endpoints (POST, GET, PUT, DELETE)
│
├── 📂 business/                          # BUSINESS LOGIC LAYER
│   ├── __init__.py
│   ├── base_model.py                     # BaseModel (UUID + timestamps)
│   ├── user.py                           # User entity
│   ├── amenity.py                        # Amenity entity
│   ├── place.py                          # Place entity
│   ├── review.py                         # Review entity
│   └── facade.py                         # HBnBFacade (orchestration)
│
├── 📂 persistence/                       # PERSISTENCE LAYER
│   ├── __init__.py
│   └── in_memory_repository.py           # In-memory data storage
│
└── 📂 tests/                             # TESTS (to be implemented)
    └── (test files here)
```

### File Descriptions

#### **app.py** (Main Application)
- Initializes Flask application
- Creates and configures the Facade
- Registers all Blueprints (routes)
- Entry point to run the server

#### **api/** (Presentation Layer)
- **users.py**: Handles User HTTP endpoints
- **amenities.py**: Handles Amenity HTTP endpoints
- **places.py**: Handles Place HTTP endpoints + special route for reviews
- **reviews.py**: Handles Review HTTP endpoints (includes DELETE)

#### **business/** (Business Logic Layer)
- **base_model.py**: Base class with common attributes (id, created_at, updated_at)
- **user.py**: User entity with email validation
- **amenity.py**: Amenity entity
- **place.py**: Place entity with price/coordinates validation
- **review.py**: Review entity with text validation
- **facade.py**: Orchestrates operations between layers

#### **persistence/** (Persistence Layer)
- **in_memory_repository.py**: Stores data in Python dictionaries during runtime

---

## Installation & Setup (English)

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **curl** (for testing)

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd holbertonschool-hbnb/part2
```

### Step 2: Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask 3.0+** (only dependency)

### Step 4: Run the Application

```bash
python app.py
```

**Expected output:**
```
======================================================================
🚀 HBnB API - Partie 2
======================================================================
📍 API : http://127.0.0.1:5000
📍 Endpoints :
   • Users     : /api/v1/users
   • Amenities : /api/v1/amenities
   • Places    : /api/v1/places
   • Reviews   : /api/v1/reviews
======================================================================
💡 Testez avec cURL ! Voir TESTING_GUIDE.md
======================================================================
```

The API is now running on **http://127.0.0.1:5000**

---

## API Endpoints (English)

### Complete Endpoint List

#### 👤 **Users** (`/api/v1/users`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| **POST** | `/api/v1/users/` | Create a new user | 201, 400 |
| **GET** | `/api/v1/users/` | List all users | 200 |
| **GET** | `/api/v1/users/<id>` | Get a specific user | 200, 404 |
| **PUT** | `/api/v1/users/<id>` | Update a user | 200, 404, 400 |

**Important:** The `password` field is **NEVER** returned in responses for security.

#### 🏠 **Amenities** (`/api/v1/amenities`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| **POST** | `/api/v1/amenities/` | Create a new amenity | 201, 400 |
| **GET** | `/api/v1/amenities/` | List all amenities | 200 |
| **GET** | `/api/v1/amenities/<id>` | Get a specific amenity | 200, 404 |
| **PUT** | `/api/v1/amenities/<id>` | Update an amenity | 200, 404, 400 |

#### 📍 **Places** (`/api/v1/places`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| **POST** | `/api/v1/places/` | Create a new place | 201, 400 |
| **GET** | `/api/v1/places/` | List all places (extended) | 200 |
| **GET** | `/api/v1/places/<id>` | Get a specific place (extended) | 200, 404 |
| **PUT** | `/api/v1/places/<id>` | Update a place | 200, 404, 400 |
| **GET** | `/api/v1/places/<id>/reviews` | **Get all reviews for a place** | 200, 404 |

**Extended Serialization:** Place responses include:
- `owner_first_name` and `owner_last_name` (owner details)
- `amenities[]` (full amenity objects, not just IDs)

#### ⭐ **Reviews** (`/api/v1/reviews`)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| **POST** | `/api/v1/reviews/` | Create a new review | 201, 400 |
| **GET** | `/api/v1/reviews/` | List all reviews | 200 |
| **GET** | `/api/v1/reviews/<id>` | Get a specific review | 200, 404 |
| **PUT** | `/api/v1/reviews/<id>` | Update a review | 200, 404, 400 |
| **DELETE** | `/api/v1/reviews/<id>` | **Delete a review** | 204, 404 |

**Special Note:** DELETE operation is **ONLY** implemented for Reviews (not for Users, Places, or Amenities).

---

## Business Logic & Validations (English)

### Entity: User

**Attributes:**
- `id` (UUID) - Unique identifier
- `email` (string, required) - Must be unique and contain `@`
- `password` (string, required) - Never exposed in API responses
- `first_name` (string, optional) - User's first name
- `last_name` (string, optional) - User's last name
- `created_at` (datetime) - Creation timestamp
- `updated_at` (datetime) - Last update timestamp

**Validations:**
- ✅ Email is required and must contain `@`
- ✅ Email must be unique (no duplicates)
- ✅ Email is automatically converted to lowercase
- ✅ Password is required
- ✅ Password is NEVER included in JSON responses

**Business Rules:**
- When updating email, uniqueness is verified (excluding current user)

---

### Entity: Amenity

**Attributes:**
- `id` (UUID) - Unique identifier
- `name` (string, required) - Amenity name (e.g., "Wi-Fi", "Pool")
- `created_at` (datetime)
- `updated_at` (datetime)

**Validations:**
- ✅ Name is required and cannot be empty

---

### Entity: Place

**Attributes:**
- `id` (UUID) - Unique identifier
- `name` (string, required) - Place name
- `description` (string, optional) - Detailed description
- `price` (float, default: 0) - Price per night
- `latitude` (float, optional) - Geographical latitude
- `longitude` (float, optional) - Geographical longitude
- `owner_id` (UUID, required) - Reference to User (owner)
- `amenity_ids` (list of UUIDs) - References to Amenities
- `reviews` (list of UUIDs) - References to Reviews
- `created_at` (datetime)
- `updated_at` (datetime)

**Validations:**
- ✅ Name is required
- ✅ Owner ID is required and must reference an existing User
- ✅ Price must be >= 0 (non-negative)
- ✅ Latitude must be between -90 and 90 (if provided)
- ✅ Longitude must be between -180 and 180 (if provided)
- ✅ All amenity IDs must reference existing Amenities

**Business Rules:**
- When creating/updating, all foreign key references are verified
- Extended serialization includes owner details and full amenity objects

---

### Entity: Review

**Attributes:**
- `id` (UUID) - Unique identifier
- `text` (string, required) - Review content
- `user_id` (UUID, required) - Reference to User (author)
- `place_id` (UUID, required) - Reference to Place
- `created_at` (datetime)
- `updated_at` (datetime)

**Validations:**
- ✅ Text is required and cannot be empty
- ✅ User ID is required and must reference an existing User
- ✅ Place ID is required and must reference an existing Place

**Business Rules:**
- When creating a review, it's automatically added to the place's review list
- When deleting a review, it's removed from the place's review list
- DELETE operation is available (unlike other entities)

---

## Testing with cURL (English)

### Basic Testing Workflow

#### 1. Create a User

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "secret123",
    "first_name": "Alice",
    "last_name": "Dupont"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Dupont",
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

⚠️ **Note:** No `password` field in response!

#### 2. List All Users

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

#### 3. Get a Specific User

```bash
curl http://127.0.0.1:5000/api/v1/users/<USER_ID>
```

#### 4. Create an Amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

#### 5. Create a Place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lakeside Chalet",
    "description": "Beautiful chalet with panoramic lake view",
    "price": 120.50,
    "latitude": 46.4,
    "longitude": 6.5,
    "owner_id": "<ALICE_USER_ID>",
    "amenity_ids": ["<WIFI_AMENITY_ID>"]
  }'
```

**Response includes extended serialization:**
```json
{
  "id": "place-uuid...",
  "name": "Lakeside Chalet",
  "price": 120.5,
  "owner_id": "...",
  "owner_first_name": "Alice",
  "owner_last_name": "Dupont",
  "amenity_ids": ["..."],
  "amenities": [
    {
      "id": "...",
      "name": "Wi-Fi",
      "created_at": "...",
      "updated_at": "..."
    }
  ],
  ...
}
```

#### 6. Create a Review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<USER_ID>",
    "place_id": "<PLACE_ID>",
    "text": "Excellent stay! Highly recommend."
  }'
```

#### 7. Get All Reviews for a Place

```bash
curl http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews
```

#### 8. Delete a Review

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>
```

**Expected Response:** `204 No Content` (empty body)

### Testing Validations (Error Cases)

#### Email Already Exists (400)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"another"}'
```

**Response:**
```json
{
  "error": "Email already exists"
}
```

#### Negative Price (400)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","owner_id":"<VALID_ID>","price":-50}'
```

**Response:**
```json
{
  "error": "Price must be >= 0"
}
```

#### Invalid Latitude (400)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","owner_id":"<VALID_ID>","latitude":100}'
```

**Response:**
```json
{
  "error": "Latitude must be between -90 and 90"
}
```

#### Resource Not Found (404)

```bash
curl http://127.0.0.1:5000/api/v1/users/fake-uuid-123
```

**Response:**
```json
{
  "error": "User not found"
}
```

---

## Code Examples (English)

### Example 1: Creating a User from Python

```python
import requests

url = "http://127.0.0.1:5000/api/v1/users/"
data = {
    "email": "bob@example.com",
    "password": "secret456",
    "first_name": "Bob",
    "last_name": "Martin"
}

response = requests.post(url, json=data)
print(response.status_code)  # 201
print(response.json())       # User object (no password)
```

### Example 2: Extended Place Serialization

When you GET a Place, the response automatically includes:

```json
{
  "id": "...",
  "name": "Lakeside Chalet",
  "price": 120.5,
  "owner_id": "user-uuid",
  "owner_first_name": "Alice",      // ← Extended
  "owner_last_name": "Dupont",      // ← Extended
  "amenity_ids": ["amenity-uuid"],
  "amenities": [                     // ← Extended (full objects)
    {
      "id": "amenity-uuid",
      "name": "Wi-Fi",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

This saves the client from making multiple requests.

### Example 3: Facade Pattern in Action

**In api/users.py:**
```python
from app import facade

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = facade.create_user(data)  # ← Facade call
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

**The Facade handles:**
1. Validating the email
2. Checking email uniqueness
3. Creating the User object
4. Storing in repository
5. Returning the created user

---

## Design Patterns (English)

### 1. Facade Pattern

**What:** `HBnBFacade` provides a simplified interface to the complex business logic.

**Why:**
- API layer doesn't need to know about repository details
- Centralized validation and business rules
- Easy to test and maintain
- Can easily swap repository implementation (e.g., in-memory → database)

**How:**
```python
# Instead of this in API:
user = User(email, password)
if repo.find_by_email(email):
    raise ValueError("Email exists")
repo.add(user)

# We do this:
user = facade.create_user(data)  # All logic hidden in Facade
```

### 2. Repository Pattern

**What:** `InMemoryRepository` abstracts data storage operations.

**Why:**
- Business logic doesn't depend on storage implementation
- Easy to switch from in-memory to database (Part 3)
- Centralized data access logic

**Methods:**
- `add(obj)` - Add object
- `get(cls, id)` - Get by ID
- `all(cls)` - Get all of a type
- `update(obj)` - Update object
- `delete(obj)` - Delete object

### 3. Blueprint Pattern (Flask)

**What:** Organizing routes into logical modules.

**Why:**
- Each entity has its own file
- Easy to find and modify routes
- Scalable architecture

**Example:**
```python
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def list_users():
    # ...
```

---

## Next Steps (Part 3) (English)

### What's Coming in Part 3?

1. **🔐 JWT Authentication**
   - Login endpoint
   - Token generation
   - Token verification on protected routes

2. **👥 Role-Based Access Control (RBAC)**
   - Admin vs regular user roles
   - Permission checks (e.g., only owner can update place)

3. **💾 Database Integration**
   - Replace in-memory repository with SQLAlchemy
   - PostgreSQL/MySQL database
   - Database migrations

4. **🔍 Advanced Features**
   - Pagination for list endpoints
   - Filtering and searching
   - More complex validations

---

---

# VERSION FRANÇAISE

## Vue d'ensemble du projet (Français)

### Qu'est-ce que HBnB ?

HBnB est une **application simplifiée de type Airbnb** conçue pour gérer :
- **Des utilisateurs** (propriétaires et évaluateurs)
- **Des lieux** (hébergements/annonces)
- **Des équipements** (commodités comme Wi-Fi, Piscine, Parking)
- **Des avis** (commentaires des utilisateurs sur les lieux)

### Objectifs de la Partie 2

Dans la **Partie 2**, nous implémentons :
1. ✅ **Couche de logique métier** (entités : User, Place, Review, Amenity)
2. ✅ **Couche de persistance** (repository en mémoire)
3. ✅ **Couche de présentation** (API RESTful avec Flask)
4. ✅ **Pattern Façade** (orchestration entre les couches)
5. ✅ **Opérations CRUD complètes** (Create, Read, Update, Delete)
6. ✅ **Validations de données** (unicité email, contraintes de prix, coordonnées, etc.)

**Pourquoi Flask pur (sans Flask-RESTX) ?**
- **Simplicité** : Une seule dépendance (Flask uniquement)
- **Contrôle** : Contrôle total sur les routes et les réponses
- **Apprentissage** : Comprendre les fondamentaux de REST
- **Testabilité** : Facile à tester avec cURL

---

## Architecture (Français)

### Architecture en 3 couches

```
┌─────────────────────────────────────────┐
│   COUCHE PRÉSENTATION (API)             │
│   - Blueprints Flask                    │
│   - Points de terminaison HTTP          │
│   - Sérialisation JSON                  │
│   - Gestion des erreurs (400, 404, etc.)│
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   COUCHE LOGIQUE MÉTIER (Façade)        │
│   - HBnBFacade (orchestration)          │
│   - Validation des entrées              │
│   - Application des règles métier       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   COUCHE DOMAINE (Entités)              │
│   - User, Place, Review, Amenity        │
│   - BaseModel (UUID + timestamps)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   COUCHE PERSISTANCE (Repository)       │
│   - InMemoryRepository                  │
│   - Opérations CRUD                     │
│   - (Deviendra SQLAlchemy en Partie 3)  │
└─────────────────────────────────────────┘
```

### Pourquoi cette architecture ?

1. **Séparation des responsabilités** : Chaque couche a une responsabilité spécifique
2. **Maintenabilité** : Facile de modifier une couche sans affecter les autres
3. **Testabilité** : Chaque couche peut être testée indépendamment
4. **Évolutivité** : Facile d'ajouter de nouvelles fonctionnalités ou de changer d'implémentation
5. **Code propre** : Dépendances et flux de données clairs

---

## Structure du projet (Français)

```
part2/
│
├── 📄 app.py                              # Point d'entrée de l'application Flask
├── 📄 requirements.txt                    # Dépendances Python (Flask uniquement)
├── 📄 README.md                          # Ce fichier (EN/FR)
├── 📄 TESTING_GUIDE.md                   # Guide de test cURL complet
├── 📄 QUICKSTART.md                      # Guide de démarrage rapide
│
├── 📂 api/                               # COUCHE PRÉSENTATION
│   ├── __init__.py
│   ├── users.py                          # Endpoints User (POST, GET, PUT)
│   ├── amenities.py                      # Endpoints Amenity (POST, GET, PUT)
│   ├── places.py                         # Endpoints Place (POST, GET, PUT, GET reviews)
│   └── reviews.py                        # Endpoints Review (POST, GET, PUT, DELETE)
│
├── 📂 business/                          # COUCHE LOGIQUE MÉTIER
│   ├── __init__.py
│   ├── base_model.py                     # BaseModel (UUID + timestamps)
│   ├── user.py                           # Entité User
│   ├── amenity.py                        # Entité Amenity
│   ├── place.py                          # Entité Place
│   ├── review.py                         # Entité Review
│   └── facade.py                         # HBnBFacade (orchestration)
│
├── 📂 persistence/                       # COUCHE PERSISTANCE
│   ├── __init__.py
│   └── in_memory_repository.py           # Stockage de données en mémoire
│
└── 📂 tests/                             # TESTS (à implémenter)
    └── (fichiers de test ici)
```

### Description des fichiers

#### **app.py** (Application principale)
- Initialise l'application Flask
- Crée et configure la Façade
- Enregistre tous les Blueprints (routes)
- Point d'entrée pour lancer le serveur

#### **api/** (Couche Présentation)
- **users.py** : Gère les endpoints HTTP pour User
- **amenities.py** : Gère les endpoints HTTP pour Amenity
- **places.py** : Gère les endpoints HTTP pour Place + route spéciale pour les reviews
- **reviews.py** : Gère les endpoints HTTP pour Review (inclut DELETE)

#### **business/** (Couche Logique Métier)
- **base_model.py** : Classe de base avec attributs communs (id, created_at, updated_at)
- **user.py** : Entité User avec validation d'email
- **amenity.py** : Entité Amenity
- **place.py** : Entité Place avec validation prix/coordonnées
- **review.py** : Entité Review avec validation du texte
- **facade.py** : Orchestre les opérations entre les couches

#### **persistence/** (Couche Persistance)
- **in_memory_repository.py** : Stocke les données dans des dictionnaires Python pendant l'exécution

---

## Installation & Configuration (Français)

### Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **curl** (pour les tests)

### Étape 1 : Cloner le dépôt

```bash
git clone <url-de-votre-dépôt>
cd holbertonschool-hbnb/part2
```

### Étape 2 : Créer un environnement virtuel

**Linux/Mac :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Cela installe :
- **Flask 3.0+** (seule dépendance)

### Étape 4 : Lancer l'application

```bash
python app.py
```

**Sortie attendue :**
```
======================================================================
🚀 HBnB API - Partie 2
======================================================================
📍 API : http://127.0.0.1:5000
📍 Endpoints :
   • Users     : /api/v1/users
   • Amenities : /api/v1/amenities
   • Places    : /api/v1/places
   • Reviews   : /api/v1/reviews
======================================================================
💡 Testez avec cURL ! Voir TESTING_GUIDE.md
======================================================================
```

L'API fonctionne maintenant sur **http://127.0.0.1:5000**

---

## Points de terminaison API (Français)

### Liste complète des endpoints

#### 👤 **Users** (`/api/v1/users`)

| Méthode | Endpoint | Description | Codes d'état |
|---------|----------|-------------|--------------|
| **POST** | `/api/v1/users/` | Créer un nouvel utilisateur | 201, 400 |
| **GET** | `/api/v1/users/` | Lister tous les utilisateurs | 200 |
| **GET** | `/api/v1/users/<id>` | Obtenir un utilisateur spécifique | 200, 404 |
| **PUT** | `/api/v1/users/<id>` | Mettre à jour un utilisateur | 200, 404, 400 |

**Important :** Le champ `password` n'est **JAMAIS** retourné dans les réponses pour la sécurité.

#### 🏠 **Amenities** (`/api/v1/amenities`)

| Méthode | Endpoint | Description | Codes d'état |
|---------|----------|-------------|--------------|
| **POST** | `/api/v1/amenities/` | Créer un nouvel équipement | 201, 400 |
| **GET** | `/api/v1/amenities/` | Lister tous les équipements | 200 |
| **GET** | `/api/v1/amenities/<id>` | Obtenir un équipement spécifique | 200, 404 |
| **PUT** | `/api/v1/amenities/<id>` | Mettre à jour un équipement | 200, 404, 400 |

#### 📍 **Places** (`/api/v1/places`)

| Méthode | Endpoint | Description | Codes d'état |
|---------|----------|-------------|--------------|
| **POST** | `/api/v1/places/` | Créer un nouveau lieu | 201, 400 |
| **GET** | `/api/v1/places/` | Lister tous les lieux (étendu) | 200 |
| **GET** | `/api/v1/places/<id>` | Obtenir un lieu spécifique (étendu) | 200, 404 |
| **PUT** | `/api/v1/places/<id>` | Mettre à jour un lieu | 200, 404, 400 |
| **GET** | `/api/v1/places/<id>/reviews` | **Obtenir tous les avis d'un lieu** | 200, 404 |

**Sérialisation étendue :** Les réponses Place incluent :
- `owner_first_name` et `owner_last_name` (détails du propriétaire)
- `amenities[]` (objets d'équipement complets, pas seulement les IDs)

#### ⭐ **Reviews** (`/api/v1/reviews`)

| Méthode | Endpoint | Description | Codes d'état |
|---------|----------|-------------|--------------|
| **POST** | `/api/v1/reviews/` | Créer un nouvel avis | 201, 400 |
| **GET** | `/api/v1/reviews/` | Lister tous les avis | 200 |
| **GET** | `/api/v1/reviews/<id>` | Obtenir un avis spécifique | 200, 404 |
| **PUT** | `/api/v1/reviews/<id>` | Mettre à jour un avis | 200, 404, 400 |
| **DELETE** | `/api/v1/reviews/<id>` | **Supprimer un avis** | 204, 404 |

**Note spéciale :** L'opération DELETE n'est implémentée **QUE** pour les Reviews (pas pour Users, Places ou Amenities).

---

## Logique métier & Validations (Français)

### Entité : User

**Attributs :**
- `id` (UUID) - Identifiant unique
- `email` (string, requis) - Doit être unique et contenir `@`
- `password` (string, requis) - Jamais exposé dans les réponses API
- `first_name` (string, optionnel) - Prénom de l'utilisateur
- `last_name` (string, optionnel) - Nom de famille
- `created_at` (datetime) - Horodatage de création
- `updated_at` (datetime) - Horodatage de dernière mise à jour

**Validations :**
- ✅ L'email est requis et doit contenir `@`
- ✅ L'email doit être unique (pas de doublons)
- ✅ L'email est automatiquement converti en minuscules
- ✅ Le mot de passe est requis
- ✅ Le mot de passe n'est JAMAIS inclus dans les réponses JSON

**Règles métier :**
- Lors de la mise à jour de l'email, l'unicité est vérifiée (en excluant l'utilisateur actuel)

---

### Entité : Amenity

**Attributs :**
- `id` (UUID) - Identifiant unique
- `name` (string, requis) - Nom de l'équipement (ex : "Wi-Fi", "Piscine")
- `created_at` (datetime)
- `updated_at` (datetime)

**Validations :**
- ✅ Le nom est requis et ne peut pas être vide

---

### Entité : Place

**Attributs :**
- `id` (UUID) - Identifiant unique
- `name` (string, requis) - Nom du lieu
- `description` (string, optionnel) - Description détaillée
- `price` (float, défaut : 0) - Prix par nuit
- `latitude` (float, optionnel) - Latitude géographique
- `longitude` (float, optionnel) - Longitude géographique
- `owner_id` (UUID, requis) - Référence à User (propriétaire)
- `amenity_ids` (liste d'UUIDs) - Références aux Amenities
- `reviews` (liste d'UUIDs) - Références aux Reviews
- `created_at` (datetime)
- `updated_at` (datetime)

**Validations :**
- ✅ Le nom est requis
- ✅ L'ID du propriétaire est requis et doit référencer un User existant
- ✅ Le prix doit être >= 0 (non négatif)
- ✅ La latitude doit être entre -90 et 90 (si fournie)
- ✅ La longitude doit être entre -180 et 180 (si fournie)
- ✅ Tous les IDs d'équipements doivent référencer des Amenities existantes

**Règles métier :**
- Lors de la création/mise à jour, toutes les références de clés étrangères sont vérifiées
- La sérialisation étendue inclut les détails du propriétaire et les objets d'équipement complets

---

### Entité : Review

**Attributs :**
- `id` (UUID) - Identifiant unique
- `text` (string, requis) - Contenu de l'avis
- `user_id` (UUID, requis) - Référence à User (auteur)
- `place_id` (UUID, requis) - Référence à Place
- `created_at` (datetime)
- `updated_at` (datetime)

**Validations :**
- ✅ Le texte est requis et ne peut pas être vide
- ✅ L'ID utilisateur est requis et doit référencer un User existant
- ✅ L'ID du lieu est requis et doit référencer un Place existant

**Règles métier :**
- Lors de la création d'un avis, il est automatiquement ajouté à la liste des avis du lieu
- Lors de la suppression d'un avis, il est retiré de la liste des avis du lieu
- L'opération DELETE est disponible (contrairement aux autres entités)

---

## Tests avec cURL (Français)

### Flux de test de base

#### 1. Créer un utilisateur

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "secret123",
    "first_name": "Alice",
    "last_name": "Dupont"
  }'
```

**Réponse attendue (201 Created) :**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Dupont",
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

⚠️ **Note :** Pas de champ `password` dans la réponse !

#### 2. Lister tous les utilisateurs

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

#### 3. Obtenir un utilisateur spécifique

```bash
curl http://127.0.0.1:5000/api/v1/users/<USER_ID>
```

#### 4. Créer un équipement

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

#### 5. Créer un lieu

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chalet au bord du lac",
    "description": "Magnifique chalet avec vue panoramique sur le lac",
    "price": 120.50,
    "latitude": 46.4,
    "longitude": 6.5,
    "owner_id": "<ALICE_USER_ID>",
    "amenity_ids": ["<WIFI_AMENITY_ID>"]
  }'
```

**La réponse inclut la sérialisation étendue :**
```json
{
  "id": "place-uuid...",
  "name": "Chalet au bord du lac",
  "price": 120.5,
  "owner_id": "...",
  "owner_first_name": "Alice",
  "owner_last_name": "Dupont",
  "amenity_ids": ["..."],
  "amenities": [
    {
      "id": "...",
      "name": "Wi-Fi",
      "created_at": "...",
      "updated_at": "..."
    }
  ],
  ...
}
```

#### 6. Créer un avis

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<USER_ID>",
    "place_id": "<PLACE_ID>",
    "text": "Excellent séjour ! Je recommande vivement."
  }'
```

#### 7. Obtenir tous les avis d'un lieu

```bash
curl http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews
```

#### 8. Supprimer un avis

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>
```

**Réponse attendue :** `204 No Content` (corps vide)

### Tester les validations (cas d'erreur)

#### Email déjà existant (400)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"autre"}'
```

**Réponse :**
```json
{
  "error": "Email already exists"
}
```

#### Prix négatif (400)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","owner_id":"<VALID_ID>","price":-50}'
```

**Réponse :**
```json
{
  "error": "Price must be >= 0"
}
```

#### Latitude invalide (400)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","owner_id":"<VALID_ID>","latitude":100}'
```

**Réponse :**
```json
{
  "error": "Latitude must be between -90 and 90"
}
```

#### Ressource non trouvée (404)

```bash
curl http://127.0.0.1:5000/api/v1/users/fake-uuid-123
```

**Réponse :**
```json
{
  "error": "User not found"
}
```

---

## Exemples de code (Français)

### Exemple 1 : Créer un utilisateur depuis Python

```python
import requests

url = "http://127.0.0.1:5000/api/v1/users/"
data = {
    "email": "bob@example.com",
    "password": "secret456",
    "first_name": "Bob",
    "last_name": "Martin"
}

response = requests.post(url, json=data)
print(response.status_code)  # 201
print(response.json())       # Objet User (sans password)
```

### Exemple 2 : Sérialisation étendue d'un Place

Lorsque vous faites un GET sur un Place, la réponse inclut automatiquement :

```json
{
  "id": "...",
  "name": "Chalet au bord du lac",
  "price": 120.5,
  "owner_id": "user-uuid",
  "owner_first_name": "Alice",      // ← Étendu
  "owner_last_name": "Dupont",      // ← Étendu
  "amenity_ids": ["amenity-uuid"],
  "amenities": [                     // ← Étendu (objets complets)
    {
      "id": "amenity-uuid",
      "name": "Wi-Fi",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

Cela évite au client de faire plusieurs requêtes.

### Exemple 3 : Pattern Façade en action

**Dans api/users.py :**
```python
from app import facade

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = facade.create_user(data)  # ← Appel à la Façade
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

**La Façade gère :**
1. La validation de l'email
2. La vérification de l'unicité de l'email
3. La création de l'objet User
4. Le stockage dans le repository
5. Le retour de l'utilisateur créé

---

## Patrons de conception (Français)

### 1. Pattern Façade

**Quoi :** `HBnBFacade` fournit une interface simplifiée pour la logique métier complexe.

**Pourquoi :**
- La couche API n'a pas besoin de connaître les détails du repository
- Validation et règles métier centralisées
- Facile à tester et à maintenir
- Possibilité de changer facilement l'implémentation du repository (ex : en mémoire → base de données)

**Comment :**
```python
# Au lieu de ceci dans l'API :
user = User(email, password)
if repo.find_by_email(email):
    raise ValueError("Email existe")
repo.add(user)

# On fait ceci :
user = facade.create_user(data)  # Toute la logique cachée dans la Façade
```

### 2. Pattern Repository

**Quoi :** `InMemoryRepository` abstrait les opérations de stockage de données.

**Pourquoi :**
- La logique métier ne dépend pas de l'implémentation du stockage
- Facile de passer de en-mémoire à base de données (Partie 3)
- Logique d'accès aux données centralisée

**Méthodes :**
- `add(obj)` - Ajouter un objet
- `get(cls, id)` - Obtenir par ID
- `all(cls)` - Obtenir tous les objets d'un type
- `update(obj)` - Mettre à jour un objet
- `delete(obj)` - Supprimer un objet

### 3. Pattern Blueprint (Flask)

**Quoi :** Organisation des routes en modules logiques.

**Pourquoi :**
- Chaque entité a son propre fichier
- Facile de trouver et modifier les routes
- Architecture évolutive

**Exemple :**
```python
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def list_users():
    # ...
```

---

## Prochaines étapes (Partie 3) (Français)

### Ce qui arrive dans la Partie 3 ?

1. **🔐 Authentification JWT**
   - Endpoint de connexion
   - Génération de token
   - Vérification de token sur les routes protégées

2. **👥 Contrôle d'accès basé sur les rôles (RBAC)**
   - Rôles admin vs utilisateur régulier
   - Vérifications de permissions (ex : seul le propriétaire peut modifier un lieu)

3. **💾 Intégration de base de données**
   - Remplacer le repository en-mémoire par SQLAlchemy
   - Base de données PostgreSQL/MySQL
   - Migrations de base de données

4. **🔍 Fonctionnalités avancées**
   - Pagination pour les endpoints de liste
   - Filtrage et recherche
   - Validations plus complexes

---

## 📚 Resources / Ressources

**English:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade)

**Français:**
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Meilleures pratiques API REST](https://restfulapi.net/)
- [Pattern Façade](https://refactoring.guru/fr/design-patterns/facade)

---

## ✨ Key Features / Fonctionnalités clés

✅ **Pure Flask** / **Flask pur** - No complex dependencies / Pas de dépendances complexes  
✅ **3-Layer Architecture** / **Architecture 3 couches** - Clean separation / Séparation propre  
✅ **Facade Pattern** / **Pattern Façade** - Simplified orchestration / Orchestration simplifiée  
✅ **Complete Validations** / **Validations complètes** - All business rules / Toutes les règles métier  
✅ **Extended Serialization** / **Sérialisation étendue** - Rich responses / Réponses enrichies  
✅ **UUID Security** / **Sécurité UUID** - Non-predictable IDs / IDs non prédictibles  
✅ **cURL Testable** / **Testable avec cURL** - Full examples provided / Exemples complets fournis  

---

**Test with cURL! See TESTING_GUIDE.md** 🚀  
**Testez avec cURL ! Voir TESTING_GUIDE.md** 🚀
