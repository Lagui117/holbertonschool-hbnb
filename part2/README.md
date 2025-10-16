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
8. [Design Patterns](#design-patterns-english)

**Français:**
1. [Vue d'ensemble du projet](#vue-densemble-du-projet-français)
2. [Architecture](#architecture-français)
3. [Structure du projet](#structure-du-projet-français)
4. [Installation & Configuration](#installation--configuration-français)
5. [Points de terminaison API](#points-de-terminaison-api-français)
6. [Logique métier & Validations](#logique-métier--validations-français)
7. [Tests avec cURL](#tests-avec-curl-français)
8. [Patrons de conception](#patrons-de-conception-français)

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

In **Part 2**, we implement a **complete RESTful API** with:
1. ✅ **API Layer** (REST endpoints with Flask)
2. ✅ **BLL - Business Logic Layer** (entities and business rules)
3. ✅ **FACADE** (orchestration pattern)
4. ✅ **PL - Persistence Layer** (in-memory repository)
5. ✅ **Complete CRUD operations**
6. ✅ **Data validations**

---

## Architecture (English)

### 4-Layer Architecture

```
┌─────────────────────────────────────────┐
│   API (Presentation Layer)              │
│   - Flask Blueprints                    │
│   - HTTP endpoints (REST)               │
│   - JSON serialization                  │
│   - Status codes (200, 201, 400, 404)  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   FACADE (Orchestration Layer)          │
│   - HBnBFacade pattern                  │
│   - Coordinates API ↔ BLL ↔ PL          │
│   - Input validation                    │
│   - Business rules enforcement          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   BLL - Business Logic Layer            │
│   - Domain entities                     │
│   - User, Place, Review, Amenity        │
│   - BaseModel (UUID + timestamps)       │
│   - Entity-level validations            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   PL - Persistence Layer                │
│   - InMemoryRepository                  │
│   - CRUD operations                     │
│   - Data storage (dictionaries)         │
│   - (SQLAlchemy in Part 3)              │
└─────────────────────────────────────────┘
```

### Layer Descriptions

**API (Presentation Layer)**
- Entry point for HTTP requests
- Routes defined with Flask Blueprints
- Handles request/response cycle
- Returns JSON with appropriate status codes

**FACADE (Orchestration Layer)**
- Central coordinator between layers
- Simplifies complex operations
- Validates business rules before persistence
- Provides clean interface to API layer

**BLL - Business Logic Layer**
- Contains domain entities (models)
- Entity-specific validations
- Business rule definitions
- Independent of persistence implementation

**PL - Persistence Layer**
- Data storage abstraction
- CRUD operations
- Currently: in-memory (dictionaries)
- Future: SQLAlchemy + Database (Part 3)

---

## Project Structure (English)

Based on your repository structure:

```
holbertonschool-hbnb/part2/
│
├── 📄 app.py                              # Flask entry point
├── 📄 requirements.txt                    # Dependencies
├── 📄 README.md                          # This file
│
├── 📂 API/                               # API LAYER (Presentation)
│   ├── __init__.py
│   ├── users.py                          # User endpoints
│   ├── amenities.py                      # Amenity endpoints
│   ├── places.py                         # Place endpoints
│   └── reviews.py                        # Review endpoints
│
├── 📂 BLL/                               # BUSINESS LOGIC LAYER
│   ├── __init__.py
│   ├── base_model.py                     # BaseModel with UUID
│   ├── user.py                           # User entity
│   ├── amenity.py                        # Amenity entity
│   ├── place.py                          # Place entity
│   └── review.py                         # Review entity
│
├── 📂 FACADE/                            # FACADE LAYER
│   ├── __init__.py
│   └── hbnb_facade.py                    # HBnBFacade orchestrator
│
└── 📂 PL/                                # PERSISTENCE LAYER
    ├── __init__.py
    └── in_memory_repository.py           # In-memory storage
```

### Folder Descriptions

#### **API/** (Presentation Layer)
Contains Flask Blueprints for each entity:
- **users.py**: POST, GET, PUT endpoints for Users
- **amenities.py**: POST, GET, PUT endpoints for Amenities
- **places.py**: POST, GET, PUT endpoints for Places + special reviews endpoint
- **reviews.py**: POST, GET, PUT, DELETE endpoints for Reviews

#### **BLL/** (Business Logic Layer)
Contains domain entities (models):
- **base_model.py**: Parent class with id, created_at, updated_at
- **user.py**: User entity with email validation
- **amenity.py**: Amenity entity
- **place.py**: Place entity with price/coordinates validation
- **review.py**: Review entity

#### **FACADE/** (Orchestration Layer)
Contains the Facade pattern implementation:
- **hbnb_facade.py**: Orchestrates operations between API, BLL, and PL

#### **PL/** (Persistence Layer)
Contains data storage:
- **in_memory_repository.py**: Repository pattern with CRUD operations

---

## Installation & Setup (English)

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **curl** (for testing)

### Installation Steps

```bash
# 1. Navigate to part2 directory
cd holbertonschool-hbnb/part2

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

The API will be running on **http://127.0.0.1:5000**

---

## API Endpoints (English)

### 👤 Users (`/api/v1/users`)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/users/` | Create user | 201, 400 |
| GET | `/api/v1/users/` | List all users | 200 |
| GET | `/api/v1/users/<id>` | Get user by ID | 200, 404 |
| PUT | `/api/v1/users/<id>` | Update user | 200, 404, 400 |

**⚠️ Important:** Password is NEVER returned in responses

### 🏠 Amenities (`/api/v1/amenities`)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/amenities/` | Create amenity | 201, 400 |
| GET | `/api/v1/amenities/` | List all amenities | 200 |
| GET | `/api/v1/amenities/<id>` | Get amenity | 200, 404 |
| PUT | `/api/v1/amenities/<id>` | Update amenity | 200, 404, 400 |

### 📍 Places (`/api/v1/places`)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/places/` | Create place | 201, 400 |
| GET | `/api/v1/places/` | List all places (extended) | 200 |
| GET | `/api/v1/places/<id>` | Get place (extended) | 200, 404 |
| PUT | `/api/v1/places/<id>` | Update place | 200, 404, 400 |
| GET | `/api/v1/places/<id>/reviews` | Get place reviews | 200, 404 |

**✨ Extended Serialization:** Includes `owner_first_name`, `owner_last_name`, and full `amenities[]` objects

### ⭐ Reviews (`/api/v1/reviews`)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/reviews/` | Create review | 201, 400 |
| GET | `/api/v1/reviews/` | List all reviews | 200 |
| GET | `/api/v1/reviews/<id>` | Get review | 200, 404 |
| PUT | `/api/v1/reviews/<id>` | Update review | 200, 404, 400 |
| DELETE | `/api/v1/reviews/<id>` | Delete review | 204, 404 |

**🗑️ Note:** DELETE is only available for Reviews

---

## Business Logic & Validations (English)

### BLL Entities

#### User
- **Attributes**: id, email, password, first_name, last_name, created_at, updated_at
- **Validations**: 
  - ✅ Email required and must contain `@`
  - ✅ Email must be unique
  - ✅ Password required
  - ✅ Password NEVER exposed in API

#### Amenity
- **Attributes**: id, name, created_at, updated_at
- **Validations**: 
  - ✅ Name required and non-empty

#### Place
- **Attributes**: id, name, description, price, latitude, longitude, owner_id, amenity_ids, created_at, updated_at
- **Validations**: 
  - ✅ Name required
  - ✅ owner_id must exist
  - ✅ price >= 0
  - ✅ latitude between -90 and 90
  - ✅ longitude between -180 and 180
  - ✅ All amenity_ids must exist

#### Review
- **Attributes**: id, text, user_id, place_id, created_at, updated_at
- **Validations**: 
  - ✅ Text required and non-empty
  - ✅ user_id must exist
  - ✅ place_id must exist

---

## Testing with cURL (English)

### Complete Test Workflow

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

**Response (201):**
```json
{
  "id": "uuid-here",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Dupont",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### 2. Create an Amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

#### 3. Create a Place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lakeside Chalet",
    "price": 100,
    "owner_id": "<alice-id>",
    "amenity_ids": ["<wifi-id>"]
  }'
```

**Response includes extended data:**
```json
{
  "id": "place-id",
  "name": "Lakeside Chalet",
  "price": 100,
  "owner_id": "alice-id",
  "owner_first_name": "Alice",
  "owner_last_name": "Dupont",
  "amenities": [
    {"id": "wifi-id", "name": "Wi-Fi", ...}
  ],
  ...
}
```

#### 4. Create a Review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user-id>",
    "place_id": "<place-id>",
    "text": "Great place!"
  }'
```

#### 5. Get Place Reviews

```bash
curl http://127.0.0.1:5000/api/v1/places/<place-id>/reviews
```

#### 6. Delete Review

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review-id>
```

**Response:** `204 No Content`

### Testing Error Cases

```bash
# Duplicate email (400)
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"test"}'

# Negative price (400)
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","owner_id":"<id>","price":-50}'

# Not found (404)
curl http://127.0.0.1:5000/api/v1/users/fake-id
```

---

## Design Patterns (English)

### 1. Facade Pattern

**Location:** `FACADE/hbnb_facade.py`

**Purpose:** Provides a simplified interface to the complex subsystems (BLL and PL)

**Benefits:**
- API doesn't need to know about BLL or PL details
- Centralized validation and business logic
- Easy to test and maintain
- Can swap PL implementation without changing API

**Example:**
```python
# API calls Facade
user = facade.create_user(data)

# Facade handles:
# 1. Validation
# 2. Business rules
# 3. Persistence
# 4. Return result
```

### 2. Repository Pattern

**Location:** `PL/in_memory_repository.py`

**Purpose:** Abstracts data storage operations

**Methods:**
- `add(obj)` - Create
- `get(cls, id)` - Read
- `all(cls)` - Read all
- `update(obj)` - Update
- `delete(obj)` - Delete

### 3. Blueprint Pattern

**Location:** `API/` folder

**Purpose:** Organize routes by entity

**Benefits:**
- Modular code organization
- Easy to find and modify routes
- Scalable architecture

---

---

# VERSION FRANÇAISE

## Vue d'ensemble du projet (Français)

### Qu'est-ce que HBnB ?

HBnB est une **application simplifiée de type Airbnb** pour gérer :
- **Utilisateurs** (propriétaires et évaluateurs)
- **Lieux** (hébergements/annonces)
- **Équipements** (commodités : Wi-Fi, Piscine, Parking)
- **Avis** (commentaires des utilisateurs)

### Objectifs Partie 2

Dans la **Partie 2**, nous implémentons une **API RESTful complète** avec :
1. ✅ **Couche API** (endpoints REST avec Flask)
2. ✅ **BLL - Business Logic Layer** (entités et règles métier)
3. ✅ **FACADE** (patron d'orchestration)
4. ✅ **PL - Persistence Layer** (repository en mémoire)
5. ✅ **Opérations CRUD complètes**
6. ✅ **Validations de données**

---

## Architecture (Français)

### Architecture en 4 couches

```
┌─────────────────────────────────────────┐
│   API (Couche Présentation)             │
│   - Blueprints Flask                    │
│   - Endpoints HTTP (REST)               │
│   - Sérialisation JSON                  │
│   - Codes statut (200, 201, 400, 404)  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   FACADE (Couche Orchestration)         │
│   - Pattern HBnBFacade                  │
│   - Coordonne API ↔ BLL ↔ PL            │
│   - Validation des entrées              │
│   - Application règles métier           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   BLL - Business Logic Layer            │
│   - Entités du domaine                  │
│   - User, Place, Review, Amenity        │
│   - BaseModel (UUID + timestamps)       │
│   - Validations niveau entité           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   PL - Persistence Layer                │
│   - InMemoryRepository                  │
│   - Opérations CRUD                     │
│   - Stockage données (dictionnaires)    │
│   - (SQLAlchemy en Partie 3)            │
└─────────────────────────────────────────┘
```

### Description des couches

**API (Couche Présentation)**
- Point d'entrée des requêtes HTTP
- Routes définies avec Flask Blueprints
- Gère le cycle requête/réponse
- Retourne JSON avec codes de statut appropriés

**FACADE (Couche Orchestration)**
- Coordinateur central entre les couches
- Simplifie les opérations complexes
- Valide les règles métier avant persistance
- Fournit interface propre à la couche API

**BLL - Business Logic Layer**
- Contient les entités du domaine (modèles)
- Validations spécifiques aux entités
- Définitions des règles métier
- Indépendant de l'implémentation de persistance

**PL - Persistence Layer**
- Abstraction du stockage de données
- Opérations CRUD
- Actuellement : en mémoire (dictionnaires)
- Futur : SQLAlchemy + Base de données (Partie 3)

---

## Structure du projet (Français)

Basée sur votre structure de dépôt :

```
holbertonschool-hbnb/part2/
│
├── 📄 app.py                              # Point d'entrée Flask
├── 📄 requirements.txt                    # Dépendances
├── 📄 README.md                          # Ce fichier
│
├── 📂 API/                               # COUCHE API (Présentation)
│   ├── __init__.py
│   ├── users.py                          # Endpoints User
│   ├── amenities.py                      # Endpoints Amenity
│   ├── places.py                         # Endpoints Place
│   └── reviews.py                        # Endpoints Review
│
├── 📂 BLL/                               # COUCHE LOGIQUE MÉTIER
│   ├── __init__.py
│   ├── base_model.py                     # BaseModel avec UUID
│   ├── user.py                           # Entité User
│   ├── amenity.py                        # Entité Amenity
│   ├── place.py                          # Entité Place
│   └── review.py                         # Entité Review
│
├── 📂 FACADE/                            # COUCHE FACADE
│   ├── __init__.py
│   └── hbnb_facade.py                    # Orchestrateur HBnBFacade
│
└── 📂 PL/                                # COUCHE PERSISTANCE
    ├── __init__.py
    └── in_memory_repository.py           # Stockage en mémoire
```

### Description des dossiers

#### **API/** (Couche Présentation)
Contient les Blueprints Flask pour chaque entité :
- **users.py** : Endpoints POST, GET, PUT pour Users
- **amenities.py** : Endpoints POST, GET, PUT pour Amenities
- **places.py** : Endpoints POST, GET, PUT pour Places + endpoint spécial reviews
- **reviews.py** : Endpoints POST, GET, PUT, DELETE pour Reviews

#### **BLL/** (Couche Logique Métier)
Contient les entités du domaine (modèles) :
- **base_model.py** : Classe parente avec id, created_at, updated_at
- **user.py** : Entité User avec validation email
- **amenity.py** : Entité Amenity
- **place.py** : Entité Place avec validation prix/coordonnées
- **review.py** : Entité Review

#### **FACADE/** (Couche Orchestration)
Contient l'implémentation du pattern Façade :
- **hbnb_facade.py** : Orchestre les opérations entre API, BLL et PL

#### **PL/** (Couche Persistance)
Contient le stockage de données :
- **in_memory_repository.py** : Pattern Repository avec opérations CRUD

---

## Installation & Configuration (Français)

### Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **curl** (pour les tests)

### Étapes d'installation

```bash
# 1. Naviguer vers le dossier part2
cd holbertonschool-hbnb/part2

# 2. Créer environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement virtuel
# Linux/Mac :
source venv/bin/activate
# Windows :
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python app.py
```

L'API sera accessible sur **http://127.0.0.1:5000**

---

## Points de terminaison API (Français)

### 👤 Users (`/api/v1/users`)

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| POST | `/api/v1/users/` | Créer utilisateur | 201, 400 |
| GET | `/api/v1/users/` | Lister tous | 200 |
| GET | `/api/v1/users/<id>` | Obtenir par ID | 200, 404 |
| PUT | `/api/v1/users/<id>` | Mettre à jour | 200, 404, 400 |

**⚠️ Important :** Password JAMAIS retourné dans les réponses

### 🏠 Amenities (`/api/v1/amenities`)

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| POST | `/api/v1/amenities/` | Créer équipement | 201, 400 |
| GET | `/api/v1/amenities/` | Lister tous | 200 |
| GET | `/api/v1/amenities/<id>` | Obtenir | 200, 404 |
| PUT | `/api/v1/amenities/<id>` | Mettre à jour | 200, 404, 400 |

### 📍 Places (`/api/v1/places`)

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| POST | `/api/v1/places/` | Créer lieu | 201, 400 |
| GET | `/api/v1/places/` | Lister tous (étendu) | 200 |
| GET | `/api/v1/places/<id>` | Obtenir (étendu) | 200, 404 |
| PUT | `/api/v1/places/<id>` | Mettre à jour | 200, 404, 400 |
| GET | `/api/v1/places/<id>/reviews` | Obtenir avis du lieu | 200, 404 |

**✨ Sérialisation étendue :** Inclut `owner_first_name`, `owner_last_name`, et objets complets `amenities[]`

### ⭐ Reviews (`/api/v1/reviews`)

| Méthode | Endpoint | Description | Statut |
|---------|----------|-------------|--------|
| POST | `/api/v1/reviews/` | Créer avis | 201, 400 |
| GET | `/api/v1/reviews/` | Lister tous | 200 |
| GET | `/api/v1/reviews/<id>` | Obtenir | 200, 404 |
| PUT | `/api/v1/reviews/<id>` | Mettre à jour | 200, 404, 400 |
| DELETE | `/api/v1/reviews/<id>` | Supprimer | 204, 404 |

**🗑️ Note :** DELETE uniquement disponible pour Reviews

---

## Logique métier & Validations (Français)

### Entités BLL

#### User
- **Attributs** : id, email, password, first_name, last_name, created_at, updated_at
- **Validations** : 
  - ✅ Email requis et doit contenir `@`
  - ✅ Email doit être unique
  - ✅ Password requis
  - ✅ Password JAMAIS exposé dans l'API

#### Amenity
- **Attributs** : id, name, created_at, updated_at
- **Validations** : 
  - ✅ Name requis et non vide

#### Place
- **Attributs** : id, name, description, price, latitude, longitude, owner_id, amenity_ids, created_at, updated_at
- **Validations** : 
  - ✅ Name requis
  - ✅ owner_id doit exister
  - ✅ price >= 0
  - ✅ latitude entre -90 et 90
  - ✅ longitude entre -180 et 180
  - ✅ Tous les amenity_ids doivent exister

#### Review
- **Attributs** : id, text, user_id, place_id, created_at, updated_at
- **Validations** : 
  - ✅ Text requis et non vide
  - ✅ user_id doit exister
  - ✅ place_id doit exister

---

## Tests avec cURL (Français)

### Flux de test complet

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

**Réponse (201) :**
```json
{
  "id": "uuid-ici",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Dupont",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### 2. Créer un équipement

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

#### 3. Créer un lieu

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chalet au bord du lac",
    "price": 100,
    "owner_id": "<alice-id>",
    "amenity_ids": ["<wifi-id>"]
  }'
```

**Réponse inclut données étendues :**
```json
{
  "id": "place-id",
  "name": "Chalet au bord du lac",
  "price": 100,
  "owner_id": "alice-id",
  "owner_first_name": "Alice",
  "owner_last_name": "Dupont",
  "amenities": [
    {"id": "wifi-id", "name": "Wi-Fi", ...}
  ],
  ...
}
```

#### 4. Créer un avis

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user-id>",
    "place_id": "<place-id>",
    "text": "Super endroit !"
  }'
```

#### 5. Obtenir les avis d'un lieu

```bash
curl http://127.0.0.1:5000/api/v1/places/<place-id>/reviews
```

#### 6. Supprimer un avis

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review-id>
```

**Réponse :** `204 No Content`

### Tests des cas d'erreur

```bash
# Email dupliqué (400)
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"test"}'

# Prix négatif (400)
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","owner_id":"<id>","price":-50}'

# Non trouvé (404)
curl http://127.0.0.1:5000/api/v1/users/fake-id
```

---

## Patrons de conception (Français)

### 1. Pattern Façade

**Emplacement :** `FACADE/hbnb_facade.py`

**Objectif :** Fournir une interface simplifiée aux sous-systèmes complexes (BLL et PL)

**Avantages :**
- L'API n'a pas besoin de connaître les détails de BLL ou PL
- Validation et logique métier centralisées
- Facile à tester et maintenir
- Possibilité de changer l'implémentation PL sans modifier l'API

**Exemple :**
```python
# L'API appelle la Façade
user = facade.create_user(data)

# La Façade gère :
# 1. Validation
# 2. Règles métier
# 3. Persistance
# 4. Retour du résultat
```

### 2. Pattern Repository

**Emplacement :** `PL/in_memory_repository.py`

**Objectif :** Abstraire les opérations de stockage de données

**Méthodes :**
- `add(obj)` - Créer
- `get(cls, id)` - Lire
- `all(cls)` - Lire tout
- `update(obj)` - Mettre à jour
- `delete(obj)` - Supprimer

### 3. Pattern Blueprint

**Emplacement :** Dossier `API/`

**Objectif :** Organiser les routes par entité

**Avantages :**
- Organisation modulaire du code
- Facile de trouver et modifier les routes
- Architecture évolutive

---

## 📚 Resources / Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade)

---

## ✨ Key Features / Fonctionnalités clés

✅ **4-Layer Architecture** / **Architecture 4 couches** (API, FACADE, BLL, PL)  
✅ **Pure Flask** / **Flask pur** - Simple & lightweight / Simple et léger  
✅ **Facade Pattern** / **Pattern Façade** - Clean orchestration / Orchestration propre  
✅ **Repository Pattern** / **Pattern Repository** - Data abstraction / Abstraction données  
✅ **Complete CRUD** / **CRUD complet** - All operations / Toutes opérations  
✅ **Validations** / **Validations** - Business rules enforced / Règles métier appliquées  
✅ **Extended Serialization** / **Sérialisation étendue** - Rich responses / Réponses enrichies  
✅ **UUID Security** / **Sécurité UUID** - Non-predictable IDs / IDs non prédictibles  

---

**See TESTING_GUIDE.md for complete cURL examples!** 🚀  
**Voir TESTING_GUIDE.md pour exemples cURL complets !** 🚀
