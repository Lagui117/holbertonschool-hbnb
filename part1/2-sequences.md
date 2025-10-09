# Sequence Diagrams for API Calls (Task 2)

Ce document regroupe les 4 diagrammes de séquence principaux de l'application HBnB.

---

## 📑 Table des matières

1. [User Registration - Inscription Utilisateur](#1-user-registration)
2. [Place Creation - Création de Lieu](#2-place-creation)
3. [Review Submission - Soumission d'Avis](#3-review-submission)
4. [Fetch Places List - Récupération Liste des Lieux](#4-fetch-places-list)

---

## 1. User Registration

### Inscription d'un nouvel utilisateur

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Facade as HBnB Facade
    participant UserService as User Service
    participant User as User Model
    participant UserRepo as User Repository
    participant DB as Database

    Note over Client,DB: EN: Presentation → Business → Persistence<br/>FR: Présentation → Métier → Persistance

    Client->>+API: POST /users {firstName, lastName, email, password}
    Note right of API: EN: Parse JSON, validate required fields<br/>FR: Parser JSON, valider champs requis

    API->>+Facade: registerUser(userData)
    Note right of Facade: EN: Single entry point to business logic<br/>FR: Point d'entrée unique vers logique métier

    Facade->>+UserService: registerUser(userData)
    
    UserService->>UserService: validateUserData(userData)
    Note right of UserService: EN: Check required fields present<br/>FR: Vérifier présence champs requis
    
    UserService->>UserService: checkEmailFormat(email)
    Note right of UserService: EN: Normalize (trim/lowercase) + validate<br/>FR: Normaliser (trim/minuscules) + valider
    
    UserService->>UserService: hashPassword(password)
    Note right of UserService: EN: Hash with bcrypt/argon2 (never plain text)<br/>FR: Hasher avec bcrypt/argon2 (jamais en clair)

    UserService->>+UserRepo: findByEmail(email)
    Note right of UserRepo: EN: Check email uniqueness<br/>FR: Vérifier unicité email
    
    UserRepo->>+DB: SELECT * FROM users WHERE email = ?
    DB-->>-UserRepo: null (not found)
    UserRepo-->>-UserService: null
    
    Note right of UserService: EN: Email available → proceed<br/>FR: Email disponible → continuer

    UserService->>+User: new User(userData)
    User->>User: generateId()
    Note right of User: EN: Generate UUID v4<br/>FR: Générer UUID v4
    
    User->>User: setCreatedAt()
    User->>User: setUpdatedAt()
    Note right of User: EN: Set timestamps for audit<br/>FR: Définir timestamps pour audit
    
    User-->>-UserService: userInstance

    UserService->>+UserRepo: save(userInstance)
    Note right of UserRepo: EN: Persist with transaction<br/>FR: Persister avec transaction
    
    UserRepo->>+DB: INSERT INTO users VALUES(...)
    DB-->>-UserRepo: success
    UserRepo-->>-UserService: savedUser

    UserService->>UserService: sanitize(savedUser)
    Note right of UserService: EN: Remove password hash<br/>FR: Retirer hash du mot de passe
    
    UserService-->>-Facade: sanitizedUser
    Facade-->>-API: sanitizedUser
    API-->>-Client: 201 Created {id, email, firstName, lastName, createdAt}

    alt Email already exists
        UserRepo-->>UserService: existingUser
        UserService-->>Facade: error EMAIL_TAKEN
        Facade-->>API: 409 Conflict
        API-->>Client: 409 {"error":"EMAIL_TAKEN"}
        
    else Invalid email format
        UserService-->>Facade: error INVALID_EMAIL
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_EMAIL"}
        
    else Weak password
        UserService-->>Facade: error WEAK_PASSWORD
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"WEAK_PASSWORD"}
        
    else DB race condition
        DB-->>UserRepo: UNIQUE VIOLATION
        UserRepo-->>UserService: dbError unique_violation
        UserService-->>Facade: error EMAIL_TAKEN
        Facade-->>API: 409 Conflict
        API-->>Client: 409 {"error":"EMAIL_TAKEN"}
        
    else Database unavailable
        DB-->>UserRepo: TIMEOUT
        UserRepo-->>UserService: dbError timeout
        UserService-->>Facade: error STORAGE_ERROR
        Facade-->>API: 503 Service Unavailable
        API-->>Client: 503 {"error":"STORAGE_ERROR"}
    end

    Note over Client,DB: DEFINITIONS FR<br/>Facade: Point entrée unique vers logique métier<br/>Hash: Transformation irréversible (bcrypt/argon2)<br/>Sanitization: Retrait champs sensibles<br/>Race condition: Conflit requêtes simultanées<br/>UUID v4: Identifiant unique (128 bits)
```

**Règles métier :**
- ✅ Email unique et valide
- ✅ Mot de passe hashé (jamais en clair)
- ✅ Timestamps automatiques (audit trail)

---

## 2. Place Creation

### Création d'un nouveau lieu par un utilisateur authentifié

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Auth as Auth Middleware
    participant Facade as HBnB Facade
    participant PlaceService as Place Service
    participant UserService as User Service
    participant Place as Place Model
    participant PlaceRepo as Place Repository
    participant DB as Database

    Note over Client,DB: EN: API+Auth → Facade → Services → Repo → DB<br/>FR: API+Auth → Facade → Services → Repo → BD

    Client->>+API: POST /places {title, description, price, lat, lng, amenities}
    Note right of API: EN: Parse JSON, check required fields<br/>FR: Parser JSON, vérifier champs requis

    API->>+Auth: validateToken(Authorization: Bearer token)
    Note right of Auth: EN: Verify JWT signature & expiry<br/>FR: Vérifier signature JWT & expiration
    Auth->>Auth: verifyJWT(token)
    Auth->>Auth: extractUserId(token)
    Auth-->>-API: userId
    Note right of Auth: EN: Authentication successful<br/>FR: Authentification réussie

    API->>+Facade: createPlace(placeData, userId)
    Note right of Facade: EN: Orchestrate services<br/>FR: Orchestrer services

    Facade->>+PlaceService: createPlace(placeData, userId)

    PlaceService->>+UserService: getUserById(userId)
    Note right of UserService: EN: Verify user exists and is active<br/>FR: Vérifier utilisateur existe et est actif
    UserService-->>-PlaceService: user

    PlaceService->>PlaceService: validatePlaceData(placeData)
    Note right of PlaceService: EN: Check title not empty<br/>FR: Vérifier titre non vide

    PlaceService->>PlaceService: validateCoordinates(lat, lng)
    Note right of PlaceService: EN: lat in [-90, 90] & lng in [-180, 180]<br/>FR: lat dans [-90, 90] & lng dans [-180, 180]

    PlaceService->>PlaceService: validatePrice(price)
    Note right of PlaceService: EN: price >= 0<br/>FR: prix >= 0

    PlaceService->>+Place: new Place(placeData, userId)

    Place->>Place: generateId()
    Note right of Place: EN: Generate UUID v4<br/>FR: Générer UUID v4

    Place->>Place: setOwner(userId)
    Place->>Place: setCreatedAt()
    Place->>Place: setUpdatedAt()
    Note right of Place: EN: Initialize entity with audit fields<br/>FR: Initialiser entité avec champs audit

    Place-->>-PlaceService: placeInstance

    PlaceService->>+PlaceRepo: save(placeInstance)
    Note right of PlaceRepo: EN: Persist within transaction<br/>FR: Persister dans une transaction

    PlaceRepo->>+DB: INSERT INTO places VALUES(...)
    DB-->>-PlaceRepo: success

    PlaceRepo-->>-PlaceService: savedPlace

    PlaceService->>PlaceService: sanitize(savedPlace)
    Note right of PlaceService: EN: Remove internal fields<br/>FR: Retirer champs internes

    PlaceService-->>-Facade: sanitizedPlace
    Facade-->>-API: sanitizedPlace
    API-->>-Client: 201 Created {id, title, price, owner, createdAt}

    alt Invalid Token
        Auth-->>API: error INVALID_TOKEN
        API-->>Client: 401 Unauthorized
        Note right of Auth: EN: Token invalid or expired<br/>FR: Token invalide ou expiré

    else User Not Found
        UserService-->>PlaceService: null
        PlaceService-->>Facade: error USER_NOT_FOUND
        Facade-->>API: 404 Not Found
        API-->>Client: 404 {"error":"USER_NOT_FOUND"}

    else Invalid Coordinates
        PlaceService-->>Facade: error INVALID_COORDINATES
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_COORDINATES"}

    else Invalid Price
        PlaceService-->>Facade: error INVALID_PRICE
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_PRICE"}

    else Database Error
        DB-->>PlaceRepo: TIMEOUT
        PlaceRepo-->>PlaceService: dbError
        PlaceService-->>Facade: error STORAGE_ERROR
        Facade-->>API: 503 Service Unavailable
        API-->>Client: 503 {"error":"STORAGE_ERROR"}
    end

    Note over Client,DB: DEFINITIONS FR<br/>JWT: Jeton signé prouvant identité<br/>Auth Middleware: Filtre validant JWT<br/>Validation: title requis, price>=0, lat[-90,90], lng[-180,180]
```

**Règles métier :**
- ✅ Authentification JWT obligatoire
- ✅ Coordonnées GPS valides
- ✅ Prix positif ou nul
- ✅ Titre obligatoire

---

## 3. Review Submission

### Soumission d'un avis par un utilisateur sur un lieu

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Auth as Auth Middleware
    participant Facade as HBnB Facade
    participant ReviewService as Review Service
    participant PlaceService as Place Service
    participant Review as Review Model
    participant ReviewRepo as Review Repository
    participant DB as Database

    Note over Client,DB: EN: API+Auth → Facade → Services → Repo → DB<br/>FR: API+Auth → Facade → Services → Repo → BD

    Client->>+API: POST /places/{placeId}/reviews {rating, comment}
    Note right of API: EN: Parse JSON, check required fields<br/>FR: Parser JSON, vérifier champs requis

    API->>+Auth: validateToken(token)
    Auth->>Auth: verifyJWT(token)
    Note right of Auth: EN: Verify JWT signature & expiry<br/>FR: Vérifier signature JWT & expiration
    Auth-->>-API: userId

    API->>+Facade: createReview(reviewData, userId, placeId)
    Note right of Facade: EN: Orchestrate services<br/>FR: Orchestrer services

    Facade->>+ReviewService: createReview(reviewData, userId, placeId)

    ReviewService->>+PlaceService: getPlaceById(placeId)
    Note right of PlaceService: EN: Verify place exists<br/>FR: Vérifier lieu existe
    PlaceService-->>-ReviewService: place

    ReviewService->>ReviewService: checkUserIsNotOwner(userId, place.ownerId)
    Note right of ReviewService: EN: Owner cannot review own place<br/>FR: Propriétaire ne peut noter son lieu

    ReviewService->>+ReviewRepo: findExistingReview(userId, placeId)
    Note right of ReviewRepo: EN: Check one review per user/place<br/>FR: Vérifier un avis par user/lieu
    ReviewRepo->>+DB: SELECT * FROM reviews WHERE userId=? AND placeId=?
    DB-->>-ReviewRepo: null
    ReviewRepo-->>-ReviewService: null

    ReviewService->>ReviewService: validateRating(rating)
    Note right of ReviewService: EN: rating in [1,5]<br/>FR: rating dans [1,5]

    ReviewService->>+Review: new Review(reviewData, userId, placeId)
    Review->>Review: generateId()
    Note right of Review: EN: Generate UUID v4<br/>FR: Générer UUID v4
    Review->>Review: setUser(userId)
    Review->>Review: setPlace(placeId)
    Review->>Review: setCreatedAt()
    Review->>Review: setUpdatedAt()
    Review-->>-ReviewService: reviewInstance

    ReviewService->>+ReviewRepo: save(reviewInstance)
    Note right of ReviewRepo: EN: Persist with transaction<br/>FR: Persister avec transaction
    ReviewRepo->>+DB: INSERT INTO reviews VALUES(...)
    DB-->>-ReviewRepo: success
    ReviewRepo-->>-ReviewService: savedReview

    ReviewService->>ReviewService: sanitize(savedReview)
    Note right of ReviewService: EN: Remove internal fields<br/>FR: Retirer champs internes

    ReviewService-->>-Facade: sanitizedReview
    Facade-->>-API: sanitizedReview
    API-->>-Client: 201 Created {id, rating, comment, createdAt}

    alt Invalid Token
        Auth-->>API: error INVALID_TOKEN
        API-->>Client: 401 Unauthorized

    else Place Not Found
        PlaceService-->>ReviewService: null
        ReviewService-->>Facade: error PLACE_NOT_FOUND
        Facade-->>API: 404 Not Found
        API-->>Client: 404 {"error":"PLACE_NOT_FOUND"}

    else Self Review Forbidden
        ReviewService-->>Facade: error FORBIDDEN_SELF_REVIEW
        Facade-->>API: 403 Forbidden
        API-->>Client: 403 {"error":"FORBIDDEN_SELF_REVIEW"}
        Note right of ReviewService: EN: Business rule violation<br/>FR: Violation règle métier

    else Duplicate Review
        ReviewRepo-->>ReviewService: existingReview
        ReviewService-->>Facade: error DUPLICATE_REVIEW
        Facade-->>API: 409 Conflict
        API-->>Client: 409 {"error":"DUPLICATE_REVIEW"}

    else Invalid Rating
        ReviewService-->>Facade: error INVALID_RATING
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_RATING"}

    else Database Error
        DB-->>ReviewRepo: TIMEOUT
        ReviewRepo-->>ReviewService: dbError
        ReviewService-->>Facade: error STORAGE_ERROR
        Facade-->>API: 503 Service Unavailable
        API-->>Client: 503 {"error":"STORAGE_ERROR"}
    end

    Note over Client,DB: DEFINITIONS FR<br/>Auto-review interdit: Propriétaire ne note pas son lieu<br/>Unicité: 1 avis max par user/lieu<br/>Rating: Entier entre 1 et 5 inclus
```

**Règles métier :**
- ❌ Pas d'auto-évaluation (propriétaire)
- ✅ Un seul avis par utilisateur/lieu
- ✅ Rating entre 1 et 5
- ✅ Authentification requise

---

## 4. Fetch Places List

### Récupération de la liste des lieux avec filtres et pagination

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as API Controller
    participant Facade as HBnB Facade
    participant PlaceService as Place Service
    participant PlaceRepo as Place Repository
    participant AmenityRepo as Amenity Repository
    participant DB as Database

    Client->>+API: GET /places?page=1&limit=10&amenities=wifi,pool
    API->>API: parseQueryParameters(query)
    API->>+Facade: getPlaces(filters, pagination)
    Facade->>+PlaceService: getPlaces(filters, pagination)
    PlaceService->>PlaceService: validateFilters(filters)
    PlaceService->>PlaceService: buildSearchCriteria(filters)
    
    PlaceService->>+PlaceRepo: findPlaces(criteria, pagination)
    PlaceRepo->>+DB: SELECT * FROM places WHERE ... LIMIT ? OFFSET ?
    DB-->>-PlaceRepo: places[]
    PlaceRepo-->>-PlaceService: places[]
    
    loop For each place
        PlaceService->>+AmenityRepo: getAmenitiesForPlace(place.id)
        AmenityRepo->>+DB: SELECT * FROM place_amenities WHERE place_id=?
        DB-->>-AmenityRepo: amenities[]
        AmenityRepo-->>-PlaceService: amenities[]
        PlaceService->>PlaceService: place.setAmenities(amenities)
    end
    Note right of PlaceService: EN: N+1 problem - consider batch fetch<br/>FR: Problème N+1 - considérer batch fetch
    
    PlaceService->>+PlaceRepo: countTotalPlaces(criteria)
    PlaceRepo->>+DB: SELECT COUNT(*) FROM places WHERE ...
    DB-->>-PlaceRepo: totalCount
    PlaceRepo-->>-PlaceService: totalCount
    
    PlaceService->>PlaceService: buildPaginationResponse(places, totalCount, pagination)
    PlaceService-->>-Facade: paginatedResponse
    Facade-->>-API: paginatedResponse
    API-->>-Client: 200 OK {items, pagination}

    alt Invalid Pagination
        PlaceService-->>Facade: error INVALID_PAGINATION
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_PAGINATION"}
        
    else Invalid Filters
        PlaceService-->>Facade: error INVALID_FILTERS
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_FILTERS"}
        
    else Database Error
        PlaceRepo-->>PlaceService: dbError
        PlaceService-->>Facade: error STORAGE_ERROR
        Facade-->>API: 503 Service Unavailable
        API-->>Client: 503 {"error":"STORAGE_ERROR"}
    end

    Note over Client,DB: DEFINITIONS FR<br/>Pagination: LIMIT=taille, OFFSET=(page-1)*limit<br/>N+1: Chaque lieu = requête amenities<br/>Solution: Batch fetch ou JOIN
```

**Fonctionnalités :**
- ✅ Pagination (page, limit)
- ✅ Filtres (prix, géolocalisation, amenities)
- ✅ Comptage total pour métadonnées
- ⚠️ Problème N+1 identifié (optimisation possible)

---

## 📊 Résumé des Codes HTTP

| Code | Signification | Utilisation |
|------|---------------|-------------|
| **200** | OK | Requête GET réussie |
| **201** | Created | Ressource créée avec succès (POST) |
| **400** | Bad Request | Données invalides (format, validation) |
| **401** | Unauthorized | Authentification manquante ou invalide |
| **403** | Forbidden | Action interdite (ex: auto-review) |
| **404** | Not Found | Ressource inexistante |
| **409** | Conflict | Conflit (ex: email déjà utilisé, avis dupliqué) |
| **503** | Service Unavailable | Service temporairement indisponible (DB down) |

---

## 🔑 Glossaire Technique

| Terme | Définition FR | Definition EN |
|-------|---------------|---------------|
| **Facade** | Point d'entrée unique qui simplifie l'accès à la logique métier | Single entry point simplifying access to business logic |
| **JWT** | JSON Web Token - jeton signé prouvant l'identité de l'utilisateur | Signed token proving user identity |
| **Hash** | Transformation irréversible d'un mot de passe (bcrypt/argon2) | Irreversible password transformation |
| **Sanitization** | Retrait des champs sensibles avant la réponse | Removal of sensitive fields before response |
| **Race Condition** | Conflit causé par deux requêtes simultanées | Conflict caused by concurrent requests |
| **UUID v4** | Identifiant unique universel (128 bits) | Universal unique identifier |
| **N+1 Problem** | Problème de performance : 1 requête + N requêtes par élément | Performance issue: 1 query + N queries per item |
| **Pagination** | Division des résultats en pages (LIMIT/OFFSET) | Result division into pages |
| **Transaction** | Opération atomique (tout réussit ou tout échoue) | Atomic operation (all or nothing) |

---

## 🎯 Flux Général de l'Application

```
┌─────────┐
│ Client  │
└────┬────┘
     │ HTTP Request (POST, GET, etc.)
     ▼
┌────────────────┐
│ API Controller │ ← Parse JSON, validate basic format
└────┬───────────┘
     │
     ▼
┌────────────────┐
│ Auth Middleware│ ← Validate JWT (if required)
└────┬───────────┘
     │
     ▼
┌────────────────┐
│  HBnB Facade   │ ← Single entry point, orchestration
└────┬───────────┘
     │
     ▼
┌────────────────┐
│    Service     │ ← Apply business rules, validations
└────┬───────────┘
     │
     ▼
┌────────────────┐
│     Model      │ ← Domain entity (User, Place, Review)
└────┬───────────┘
     │
     ▼
┌────────────────┐
│   Repository   │ ← Data access abstraction
└────┬───────────┘
     │
     ▼
┌────────────────┐
│    Database    │ ← Persistent storage
└────────────────┘
     │
     └─── Response flows back upward ───┐
                                        │
                                        ▼
                                   ┌─────────┐
                                   │ Client  │
                                   └─────────┘
```

---

## ✅ Principes Architecturaux Appliqués

### Séparation des Responsabilités
- **Présentation** : Gestion HTTP, parsing, validation basique
- **Logique Métier** : Règles business, orchestration
- **Persistance** : Accès données, transactions

### Pattern Facade
- Point d'entrée unique vers la logique métier
- Simplifie les interactions entre couches
- Standardise la gestion des erreurs

### Validation Multi-Niveaux
1. **API** : Format JSON, champs requis
2. **Service** : Règles métier (email unique, prix positif, etc.)
3. **Database** : Contraintes d'intégrité (UNIQUE, NOT NULL, etc.)

### Sécurité
- Authentification JWT pour opérations sensibles
- Mots de passe hashés (jamais en clair)
- Sanitization des réponses (pas de données sensibles)
- Validation stricte des entrées utilisateur