# HBnB Part 3 - API Testing Guide

## Démarrage rapide / Quick Start

### 1. Installation

```bash
cd /workspaces/holbertonschool-hbnb/part3
python3 -m venv hbnbvenv
source hbnbvenv/bin/activate
pip install -r requirements.txt
```

### 2. Initialiser la base de données

```bash
python create_first_admin.py
```

**Admin créé par défaut:**
- Email: `admin@hbnb.io`
- Password: `admin1234`

### 3. Démarrer le serveur

```bash
python run.py
```

Le serveur démarre sur `http://127.0.0.1:5000/`

### 4. Documentation Swagger

Accédez à la documentation interactive Swagger à l'adresse: `http://127.0.0.1:5000/`

---

## Tests des Endpoints

### Authentification

#### Login (Public)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin1234"}'
```

**Réponse:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Utilisation du token:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/api/v1/...
```

---

### Gestion des Utilisateurs

#### Créer un utilisateur standard (Public)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### Créer un utilisateur admin (Admin uniquement)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "newadmin@hbnb.io",
    "password": "admin123",
    "is_admin": true
  }'
```

#### Lister tous les utilisateurs (Admin uniquement)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

#### Obtenir un utilisateur (Authentifié - Self ou Admin)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/1 \
  -H "Authorization: Bearer $TOKEN"
```

#### Mettre à jour un utilisateur (Authentifié - Self ou Admin)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith"
  }'
```

#### Modification complète admin (Admin uniquement)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/1/admin-update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "newemail@hbnb.io",
    "password": "newpassword",
    "is_admin": true
  }'
```

#### Supprimer un utilisateur (Authentifié - Self ou Admin)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/users/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

### Gestion des Amenities

#### Créer une amenity (Admin uniquement)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name": "WiFi"}'
```

#### Lister toutes les amenities (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

#### Obtenir une amenity (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/1
```

#### Mettre à jour une amenity (Admin uniquement)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name": "High-Speed WiFi"}'
```

---

### Gestion des Places

#### Créer un place (Authentifié)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Beautiful Beach House",
    "description": "Amazing sea view",
    "price": 150.0,
    "latitude": 45.5,
    "longitude": -73.6,
    "amenities": [1, 2]
  }'
```

**Note:** `owner_id` est automatiquement défini à partir du JWT

#### Lister tous les places (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/
```

#### Obtenir un place (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/1
```

#### Mettre à jour un place (Owner ou Admin)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/places/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Updated Title",
    "price": 200.0
  }'
```

#### Supprimer un place (Owner ou Admin)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/places/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

### Gestion des Reviews

#### Créer un review (Authentifié)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "1"
  }'
```

**Restrictions:**
- Impossible de reviewer sa propre place
- Un utilisateur ne peut reviewer un place qu'une seule fois

#### Lister tous les reviews (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```

#### Obtenir un review (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/1
```

#### Lister les reviews d'un place (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/places/1/reviews
```

#### Mettre à jour un review (Creator ou Admin)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Updated review",
    "rating": 4
  }'
```

#### Supprimer un review (Creator ou Admin)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Matrice des Permissions

| Endpoint | Public | Authentifié | Owner | Admin |
|----------|--------|-------------|-------|-------|
| **Auth** |
| POST /auth/login | ✅ | ✅ | ✅ | ✅ |
| **Users** |
| POST /users/ (standard) | ✅ | ✅ | ✅ | ✅ |
| POST /users/ (admin) | ❌ | ❌ | ❌ | ✅ |
| GET /users/ | ❌ | ❌ | ❌ | ✅ |
| GET /users/:id | ❌ | ✅ (self) | - | ✅ |
| PUT /users/:id | ❌ | ✅ (self) | - | ✅ |
| PUT /users/:id/admin-update | ❌ | ❌ | ❌ | ✅ |
| DELETE /users/:id | ❌ | ✅ (self) | - | ✅ |
| **Amenities** |
| POST /amenities/ | ❌ | ❌ | ❌ | ✅ |
| GET /amenities/ | ✅ | ✅ | ✅ | ✅ |
| GET /amenities/:id | ✅ | ✅ | ✅ | ✅ |
| PUT /amenities/:id | ❌ | ❌ | ❌ | ✅ |
| **Places** |
| POST /places/ | ❌ | ✅ | - | ✅ |
| GET /places/ | ✅ | ✅ | ✅ | ✅ |
| GET /places/:id | ✅ | ✅ | ✅ | ✅ |
| PUT /places/:id | ❌ | ❌ | ✅ | ✅ |
| DELETE /places/:id | ❌ | ❌ | ✅ | ✅ |
| **Reviews** |
| POST /reviews/ | ❌ | ✅ | - | ✅ |
| GET /reviews/ | ✅ | ✅ | ✅ | ✅ |
| GET /reviews/:id | ✅ | ✅ | ✅ | ✅ |
| GET /reviews/places/:id/reviews | ✅ | ✅ | ✅ | ✅ |
| PUT /reviews/:id | ❌ | ✅ (creator) | - | ✅ |
| DELETE /reviews/:id | ❌ | ✅ (creator) | - | ✅ |

---

## Règles Métier

### Utilisateurs
- Mot de passe hashé avec bcrypt
- Email unique
- `is_admin` ne peut être défini que par un admin

### Places
- Latitude: -90 à 90
- Longitude: -180 à 180
- Prix: >= 0
- Owner défini automatiquement depuis le JWT

### Reviews
- Rating: 1 à 5
- Impossible de reviewer sa propre place
- Un utilisateur ne peut reviewer un place qu'une fois
- Contrainte UNIQUE(user_id, place_id) dans la DB

### Amenities
- Nom unique
- Longueur max: 50 caractères

---

## Codes de Réponse HTTP

| Code | Signification |
|------|--------------|
| 200 | OK - Succès |
| 201 | Created - Ressource créée |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - JWT manquant ou invalide |
| 403 | Forbidden - Permissions insuffisantes |
| 404 | Not Found - Ressource non trouvée |
| 500 | Internal Server Error - Erreur serveur |

---

## Configuration

### Fichier `config.py`

```python
# Environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///development.db')
```

### Variables d'environnement recommandées

```bash
export SECRET_KEY='your-very-secret-key'
export JWT_SECRET_KEY='your-jwt-secret-key'
export DEV_DATABASE_URI='sqlite:///development.db'
```

---

## Base de Données

### Schéma SQLite (Development)

Les tables sont créées automatiquement au démarrage avec `db.create_all()`.

### Migration vers MySQL (Production)

1. Installer PyMySQL:
```bash
pip install pymysql
```

2. Modifier `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/hbnb_db'
```

3. Créer la base de données:
```sql
CREATE DATABASE hbnb_db;
```

### Script SQL manuel

Pour créer la base manuellement:
```bash
sqlite3 development.db < setup.sql
```

---

## Structure du Projet

```
part3/
├── app/
│   ├── __init__.py                # Application Factory
│   ├── extensions.py              # Extensions (db, bcrypt, jwt)
│   ├── models/                    # Modèles SQLAlchemy
│   │   ├── base_model.py          # BaseModel abstrait
│   │   ├── user.py                # User avec bcrypt
│   │   ├── place.py               # Place avec relations
│   │   ├── review.py              # Review
│   │   └── amenity.py             # Amenity
│   ├── persistence/               # Repositories
│   │   ├── repository.py          # SQLAlchemyRepository
│   │   ├── user_repository.py     # UserRepository
│   │   ├── place_repository.py    # PlaceRepository (pas utilisé)
│   │   ├── review_repository.py   # ReviewRepository (pas utilisé)
│   │   └── amenity_repository.py  # AmenityRepository (pas utilisé)
│   ├── services/
│   │   └── facade.py              # HBnBFacade (Business Logic)
│   └── api/
│       └── v1/
│           ├── __init__.py        # Facade partagée
│           ├── auth.py            # Login endpoint
│           ├── users.py           # Endpoints utilisateurs
│           ├── places.py          # Endpoints places
│           ├── reviews.py         # Endpoints reviews
│           ├── amenities.py       # Endpoints amenities
│           └── protector.py       # Endpoint protégé exemple
├── config.py                      # Configuration
├── requirements.txt               # Dépendances
├── run.py                         # Point d'entrée
├── create_first_admin.py          # Script init admin
├── setup.sql                      # Script SQL manuel
├── ER_diag.md                     # Diagramme ER
└── API_TESTING.md                 # Ce fichier

```

---

## Dépannage

### "ModuleNotFoundError: No module named 'flask'"

```bash
source hbnbvenv/bin/activate
pip install -r requirements.txt
```

### "401 Unauthorized"

Vérifiez que le token JWT est valide et inclus dans l'header:
```bash
curl -H "Authorization: Bearer $TOKEN" ...
```

### "403 Forbidden"

Vérifiez que vous avez les permissions nécessaires (admin, owner, etc.)

### Base de données corrompue

```bash
rm development.db
python create_first_admin.py
```

---

## Auteur

Projet HBnB - Part 3  
Enhanced Backend with Authentication and Database Integration
