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
    participant API
    participant Facade
    participant UserService
    participant UserRepo
    participant DB

    Client->>+API: POST /users {firstName, lastName, email, password}
    API->>+Facade: registerUser(userData)
    Facade->>+UserService: registerUser(userData)
    
    UserService->>UserService: validateEmail(email)
    UserService->>UserService: hashPassword(password)
    
    UserService->>+UserRepo: findByEmail(email)
    UserRepo->>+DB: SELECT WHERE email = ?
    DB-->>-UserRepo: null
    UserRepo-->>-UserService: null
    
    UserService->>UserService: createUser(userData)
    UserService->>+UserRepo: save(user)
    UserRepo->>+DB: INSERT INTO users
    DB-->>-UserRepo: success
    UserRepo-->>-UserService: savedUser
    
    UserService-->>-Facade: sanitizedUser
    Facade-->>-API: sanitizedUser
    API-->>-Client: 201 Created

    alt Email exists
        UserRepo-->>UserService: existingUser
        UserService-->>Facade: error EMAIL_TAKEN
        Facade-->>API: 409 Conflict
        API-->>Client: 409 Conflict
    else Invalid data
        UserService-->>Facade: error INVALID_DATA
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 Bad Request
    end
```

**Règles :** Email unique, mot de passe hashé, validation des données

---

## 2. Place Creation

### Création d'un nouveau lieu

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API
    participant Auth
    participant Facade
    participant PlaceService
    participant PlaceRepo
    participant DB

    Client->>+API: POST /places {title, price, lat, lng}
    API->>+Auth: validateToken(token)
    Auth-->>-API: userId
    
    API->>+Facade: createPlace(placeData, userId)
    Facade->>+PlaceService: createPlace(placeData, userId)
    
    PlaceService->>PlaceService: validateCoordinates(lat, lng)
    PlaceService->>PlaceService: validatePrice(price)
    
    PlaceService->>PlaceService: createPlace(data, userId)
    PlaceService->>+PlaceRepo: save(place)
    PlaceRepo->>+DB: INSERT INTO places
    DB-->>-PlaceRepo: success
    PlaceRepo-->>-PlaceService: savedPlace
    
    PlaceService-->>-Facade: sanitizedPlace
    Facade-->>-API: sanitizedPlace
    API-->>-Client: 201 Created

    alt Invalid token
        Auth-->>API: error INVALID_TOKEN
        API-->>Client: 401 Unauthorized
    else Invalid data
        PlaceService-->>Facade: error INVALID_DATA
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 Bad Request
    end
```

**Règles :** JWT requis, coordonnées valides, prix ≥ 0

---

## 3. Review Submission

### Soumission d'un avis

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API
    participant Auth
    participant Facade
    participant ReviewService
    participant ReviewRepo
    participant DB

    Client->>+API: POST /places/{placeId}/reviews {rating, comment}
    API->>+Auth: validateToken(token)
    Auth-->>-API: userId
    
    API->>+Facade: createReview(data, userId, placeId)
    Facade->>+ReviewService: createReview(data, userId, placeId)
    
    ReviewService->>ReviewService: checkNotOwner(userId, placeId)
    ReviewService->>+ReviewRepo: findExisting(userId, placeId)
    ReviewRepo->>+DB: SELECT WHERE userId=? AND placeId=?
    DB-->>-ReviewRepo: null
    ReviewRepo-->>-ReviewService: null
    
    ReviewService->>ReviewService: validateRating(rating)
    ReviewService->>ReviewService: createReview(data)
    
    ReviewService->>+ReviewRepo: save(review)
    ReviewRepo->>+DB: INSERT INTO reviews
    DB-->>-ReviewRepo: success
    ReviewRepo-->>-ReviewService: savedReview
    
    ReviewService-->>-Facade: sanitizedReview
    Facade-->>-API: sanitizedReview
    API-->>-Client: 201 Created

    alt Self-review
        ReviewService-->>Facade: error SELF_REVIEW
        Facade-->>API: 403 Forbidden
        API-->>Client: 403 Forbidden
    else Duplicate
        ReviewRepo-->>ReviewService: existingReview
        ReviewService-->>Facade: error DUPLICATE
        Facade-->>API: 409 Conflict
        API-->>Client: 409 Conflict
    end
```

**Règles :** Pas d'auto-review, 1 avis par lieu, rating 1-5

---

## 4. Fetch Places List

### Récupération liste des lieux

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API
    participant Facade
    participant PlaceService
    participant PlaceRepo
    participant DB

    Client->>+API: GET /places?page=1&limit=10
    API->>+Facade: getPlaces(filters, pagination)
    Facade->>+PlaceService: getPlaces(filters, pagination)
    
    PlaceService->>+PlaceRepo: findPlaces(criteria, pagination)
    PlaceRepo->>+DB: SELECT * FROM places LIMIT ? OFFSET ?
    DB-->>-PlaceRepo: places[]
    PlaceRepo-->>-PlaceService: places[]
    
    PlaceService->>+PlaceRepo: countTotal(criteria)
    PlaceRepo->>+DB: SELECT COUNT(*)
    DB-->>-PlaceRepo: count
    PlaceRepo-->>-PlaceService: count
    
    PlaceService->>PlaceService: buildPaginationResponse()
    PlaceService-->>-Facade: response
    Facade-->>-API: response
    API-->>-Client: 200 OK {items, pagination}

    alt Invalid params
        PlaceService-->>Facade: error INVALID_PARAMS
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 Bad Request
    end
```

**Fonctionnalités :** Pagination, filtres, comptage total

---

## 📊 Codes HTTP

| Code | Usage |
|------|-------|
| 200 | GET réussi |
| 201 | POST réussi (ressource créée) |
| 400 | Données invalides |
| 401 | Non authentifié |
| 403 | Action interdite |
| 404 | Ressource inexistante |
| 409 | Conflit (email/avis dupliqué) |
| 503 | Service indisponible |

---

## 🔑 Concepts Clés

**Facade** : Point d'entrée unique vers la logique métier

**JWT** : Token d'authentification signé

**Validation** : Email unique, prix ≥ 0, rating 1-5, coordonnées GPS valides

**Règles métier** : 
- Pas d'auto-évaluation
- Un avis par utilisateur/lieu
- Mot de passe hashé (jamais en clair)

---

## 🎯 Flux Général

```
Client → API → Auth (si requis) → Facade → Service → Repository → Database
```