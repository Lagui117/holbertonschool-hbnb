 HBnB Part  - API Testing Guide

 Dmarrage rapide / Quick Start

 . Installation

```bash
cd /workspaces/holbertonschool-hbnb/part
python -m venv hbnbvenv
source hbnbvenv/bin/activate
pip install -r requirements.txt
```

 . Initialiser la base de donnes

```bash
python create_first_admin.py
```

Admin cr par dfaut:
- Email: `admin@hbnb.io`
- Password: `admin`

 . Dmarrer le serveur

```bash
python run.py
```

Le serveur dmarre sur `http://...:/`

 . Documentation Swagger

Accdez à la documentation interactive Swagger à l'adresse: `http://...:/`

---

 Tests des Endpoints

 Authentification

 Login (Public)

```bash
curl -X POST http://...:/api/v/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin"}'
```

Rponse:
```json
{
  "access_token": "eyJhbGciOiJIUzINiIsInRcCIIkpXVCJ..."
}
```

Utilisation du token:
```bash
TOKEN="eyJhbGciOiJIUzINiIsInRcCIIkpXVCJ..."
curl -H "Authorization: Bearer $TOKEN" http://...:/api/v/...
```

---

 Gestion des Utilisateurs

 Crer un utilisateur standard (Public)

```bash
curl -X POST http://...:/api/v/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "password"
  }'
```

 Crer un utilisateur admin (Admin uniquement)

```bash
curl -X POST http://...:/api/v/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "Admin",
    "last_name": "User",
    "email": "newadmin@hbnb.io",
    "password": "admin",
    "is_admin": true
  }'
```

 Lister tous les utilisateurs (Admin uniquement)

```bash
curl -X GET http://...:/api/v/users/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

 Obtenir un utilisateur (Authentifi - Self ou Admin)

```bash
curl -X GET http://...:/api/v/users/ \
  -H "Authorization: Bearer $TOKEN"
```

 Mettre à jour un utilisateur (Authentifi - Self ou Admin)

```bash
curl -X PUT http://...:/api/v/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith"
  }'
```

 Modification complète admin (Admin uniquement)

```bash
curl -X PUT http://...:/api/v/users//admin-update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "newemail@hbnb.io",
    "password": "newpassword",
    "is_admin": true
  }'
```

 Supprimer un utilisateur (Authentifi - Self ou Admin)

```bash
curl -X DELETE http://...:/api/v/users/ \
  -H "Authorization: Bearer $TOKEN"
```

---

 Gestion des Amenities

 Crer une amenity (Admin uniquement)

```bash
curl -X POST http://...:/api/v/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name": "WiFi"}'
```

 Lister toutes les amenities (Public)

```bash
curl -X GET http://...:/api/v/amenities/
```

 Obtenir une amenity (Public)

```bash
curl -X GET http://...:/api/v/amenities/
```

 Mettre à jour une amenity (Admin uniquement)

```bash
curl -X PUT http://...:/api/v/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name": "High-Speed WiFi"}'
```

---

 Gestion des Places

 Crer un place (Authentifi)

```bash
curl -X POST http://...:/api/v/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Beautiful Beach House",
    "description": "Amazing sea view",
    "price": .,
    "latitude": .,
    "longitude": -.,
    "amenities": [, ]
  }'
```

Note: `owner_id` est automatiquement dfini à partir du JWT

 Lister tous les places (Public)

```bash
curl -X GET http://...:/api/v/places/
```

 Obtenir un place (Public)

```bash
curl -X GET http://...:/api/v/places/
```

 Mettre à jour un place (Owner ou Admin)

```bash
curl -X PUT http://...:/api/v/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Updated Title",
    "price": .
  }'
```

 Supprimer un place (Owner ou Admin)

```bash
curl -X DELETE http://...:/api/v/places/ \
  -H "Authorization: Bearer $TOKEN"
```

---

 Gestion des Reviews

 Crer un review (Authentifi)

```bash
curl -X POST http://...:/api/v/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Great place!",
    "rating": ,
    "place_id": ""
  }'
```

Restrictions:
- Impossible de reviewer sa propre place
- Un utilisateur ne peut reviewer un place qu'une seule fois

 Lister tous les reviews (Public)

```bash
curl -X GET http://...:/api/v/reviews/
```

 Obtenir un review (Public)

```bash
curl -X GET http://...:/api/v/reviews/
```

 Lister les reviews d'un place (Public)

```bash
curl -X GET http://...:/api/v/reviews/places//reviews
```

 Mettre à jour un review (Creator ou Admin)

```bash
curl -X PUT http://...:/api/v/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Updated review",
    "rating": 
  }'
```

 Supprimer un review (Creator ou Admin)

```bash
curl -X DELETE http://...:/api/v/reviews/ \
  -H "Authorization: Bearer $TOKEN"
```

---

 Matrice des Permissions

| Endpoint | Public | Authentifi | Owner | Admin |
|----------|--------|-------------|-------|-------|
| Auth |
| POST /auth/login |  |  |  |  |
| Users |
| POST /users/ (standard) |  |  |  |  |
| POST /users/ (admin) |  |  |  |  |
| GET /users/ |  |  |  |  |
| GET /users/:id |  |  (self) | - |  |
| PUT /users/:id |  |  (self) | - |  |
| PUT /users/:id/admin-update |  |  |  |  |
| DELETE /users/:id |  |  (self) | - |  |
| Amenities |
| POST /amenities/ |  |  |  |  |
| GET /amenities/ |  |  |  |  |
| GET /amenities/:id |  |  |  |  |
| PUT /amenities/:id |  |  |  |  |
| Places |
| POST /places/ |  |  | - |  |
| GET /places/ |  |  |  |  |
| GET /places/:id |  |  |  |  |
| PUT /places/:id |  |  |  |  |
| DELETE /places/:id |  |  |  |  |
| Reviews |
| POST /reviews/ |  |  | - |  |
| GET /reviews/ |  |  |  |  |
| GET /reviews/:id |  |  |  |  |
| GET /reviews/places/:id/reviews |  |  |  |  |
| PUT /reviews/:id |  |  (creator) | - |  |
| DELETE /reviews/:id |  |  (creator) | - |  |

---

 Règles Mtier

 Utilisateurs
- Mot de passe hash avec bcrypt
- Email unique
- `is_admin` ne peut être dfini que par un admin

 Places
- Latitude: - à 
- Longitude: - à 
- Prix: >= 
- Owner dfini automatiquement depuis le JWT

 Reviews
- Rating:  à 
- Impossible de reviewer sa propre place
- Un utilisateur ne peut reviewer un place qu'une fois
- Contrainte UNIQUE(user_id, place_id) dans la DB

 Amenities
- Nom unique
- Longueur max:  caractères

---

 Codes de Rponse HTTP

| Code | Signification |
|------|--------------|
|  | OK - Succès |
|  | Created - Ressource cre |
|  | Bad Request - Donnes invalides |
|  | Unauthorized - JWT manquant ou invalide |
|  | Forbidden - Permissions insuffisantes |
|  | Not Found - Ressource non trouve |
|  | Internal Server Error - Erreur serveur |

---

 Configuration

 Fichier `config.py`

```python
 Environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///development.db')
```

 Variables d'environnement recommandes

```bash
export SECRET_KEY='your-very-secret-key'
export JWT_SECRET_KEY='your-jwt-secret-key'
export DEV_DATABASE_URI='sqlite:///development.db'
```

---

 Base de Donnes

 Schma SQLite (Development)

Les tables sont cres automatiquement au dmarrage avec `db.create_all()`.

 Migration vers MySQL (Production)

. Installer PyMySQL:
```bash
pip install pymysql
```

. Modifier `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/hbnb_db'
```

. Crer la base de donnes:
```sql
CREATE DATABASE hbnb_db;
```

 Script SQL manuel

Pour crer la base manuellement:
```bash
sqlite development.db < setup.sql
```

---

 Structure du Projet

```
part/
 app/
    __init__.py                 Application Factory
    extensions.py               Extensions (db, bcrypt, jwt)
    models/                     Modèles SQLAlchemy
       base_model.py           BaseModel abstrait
       user.py                 User avec bcrypt
       place.py                Place avec relations
       review.py               Review
       amenity.py              Amenity
    persistence/                Repositories
       repository.py           SQLAlchemyRepository
       user_repository.py      UserRepository
       place_repository.py     PlaceRepository (pas utilis)
       review_repository.py    ReviewRepository (pas utilis)
       amenity_repository.py   AmenityRepository (pas utilis)
    services/
       facade.py               HBnBFacade (Business Logic)
    api/
        v/
            __init__.py         Facade partage
            auth.py             Login endpoint
            users.py            Endpoints utilisateurs
            places.py           Endpoints places
            reviews.py          Endpoints reviews
            amenities.py        Endpoints amenities
            protector.py        Endpoint protg exemple
 config.py                       Configuration
 requirements.txt                Dpendances
 run.py                          Point d'entre
 create_first_admin.py           Script init admin
 setup.sql                       Script SQL manuel
 ER_diag.md                      Diagramme ER
 API_TESTING.md                  Ce fichier

```

---

 Dpannage

 "ModuleNotFoundError: No module named 'flask'"

```bash
source hbnbvenv/bin/activate
pip install -r requirements.txt
```

 " Unauthorized"

Vrifiez que le token JWT est valide et inclus dans l'header:
```bash
curl -H "Authorization: Bearer $TOKEN" ...
```

 " Forbidden"

Vrifiez que vous avez les permissions ncessaires (admin, owner, etc.)

 Base de donnes corrompue

```bash
rm development.db
python create_first_admin.py
```

---

 Auteur

Projet HBnB - Part   
Enhanced Backend with Authentication and Database Integration
