# Sequence Diagrams for API Calls (Task 2)

##  Table des matières / Table of Contents

1. [User Registration – Inscription utilisateur](#1-user-registration)
2. [Place Creation – Création de lieu](#2-place-creation)
3. [Review Submission – Soumission d'avis](#3-review-submission)
4. [Fetch Places List – Récupération de la liste des lieux](#4-fetch-places-list)

---

## 1⃣ User Registration – Inscription utilisateur

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API
    participant Facade
    participant UserService
    participant UserRepo
    participant DB

    %% ==== FLUX PRINCIPAL / MAIN FLOW ====
    Client->>+API: POST /users {firstName, lastName, email, password}
    API->>+Facade: registerUser(userData)
    Facade->>+UserService: registerUser(userData)
    
    UserService->>UserService: validateEmail(email)
    UserService->>UserService: hashPassword(password)
    
    UserService->>+UserRepo: findByEmail(email)
    UserRepo->>+DB: SELECT * FROM users WHERE email = ?
    DB-->>-UserRepo: 
    UserRepo-->>-UserService: 
    
    UserService->>UserService: createUser(userData)
    UserService->>+UserRepo: save(user)
    UserRepo->>+DB: INSERT INTO users VALUES (...)
    DB-->>-UserRepo: success
    UserRepo-->>-UserService: savedUser
    
    UserService-->>-Facade: sanitizedUser
    Facade-->>-API: sanitizedUser
    API-->>-Client: 201 Created

    %% ==== ALTERNATIVE FLOWS ====
    alt Email already exists
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

 **FR :** Vérifie l'unicité de l'email, hache le mot de passe avant stockage.  
 **EN :** Checks unique email, hashes password before saving.

---

## 2⃣ Place Creation – Création de lieu

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

    %% ==== FLUX PRINCIPAL / MAIN FLOW ====
    Client->>+API: POST /places {title, price, lat, lng}
    API->>+Auth: validateToken(token)
    Auth-->>-API: userId
    
    API->>+Facade: createPlace(placeData, userId)
    Facade->>+PlaceService: createPlace(placeData, userId)
    
    PlaceService->>PlaceService: validateCoordinates(lat, lng)
    PlaceService->>PlaceService: validatePrice(price)
    
    PlaceService->>+PlaceRepo: save(place)
    PlaceRepo->>+DB: INSERT INTO places VALUES (...)
    DB-->>-PlaceRepo: success
    PlaceRepo-->>-PlaceService: savedPlace
    
    PlaceService-->>-Facade: sanitizedPlace
    Facade-->>-API: sanitizedPlace
    API-->>-Client: 201 Created

    %% ==== ALTERNATIVES ====
    alt Invalid token
        Auth-->>API: error INVALID_TOKEN
        API-->>Client: 401 Unauthorized
    else Invalid data
        PlaceService-->>Facade: error INVALID_DATA
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 Bad Request
    end
```

 **FR :** JWT requis, coordonnées valides, prix ≥ 0.  
 **EN :** JWT required, valid coordinates, price ≥ 0.

---

## 3⃣ Review Submission – Soumission d'avis

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

    %% ==== FLUX PRINCIPAL / MAIN FLOW ====
    Client->>+API: POST /places/{placeId}/reviews {rating, comment}
    API->>+Auth: validateToken(token)
    Auth-->>-API: userId
    
    API->>+Facade: createReview(data, userId, placeId)
    Facade->>+ReviewService: createReview(data, userId, placeId)
    
    ReviewService->>ReviewService: checkNotOwner(userId, placeId)
    ReviewService->>+ReviewRepo: findExisting(userId, placeId)
    ReviewRepo->>+DB: SELECT * FROM reviews WHERE userId=? AND placeId=?
    DB-->>-ReviewRepo: null
    ReviewRepo-->>-ReviewService: null
    
    ReviewService->>ReviewService: validateRating(rating)
    ReviewService->>+ReviewRepo: save(review)
    ReviewRepo->>+DB: INSERT INTO reviews VALUES (...)
    DB-->>-ReviewRepo: success
    ReviewRepo-->>-ReviewService: savedReview
    
    ReviewService-->>-Facade: sanitizedReview
    Facade-->>-API: sanitizedReview
    API-->>-Client: 201 Created

    %% ==== ERREURS ====
    alt Self-review
        ReviewService-->>Facade: error SELF_REVIEW
        Facade-->>API: 403 Forbidden
        API-->>Client: 403 Forbidden
    else Duplicate review
        ReviewRepo-->>ReviewService: existingReview
        ReviewService-->>Facade: error DUPLICATE
        Facade-->>API: 409 Conflict
        API-->>Client: 409 Conflict
    end
```

 **FR :** Un utilisateur ne peut pas noter son propre lieu, un seul avis par lieu.  
 **EN :** User cannot review their own place, one review per place only.

---

## 4⃣ Fetch Places List – Récupération de la liste des lieux

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API
    participant Facade
    participant PlaceService
    participant PlaceRepo
    participant DB

    %% ==== FLUX PRINCIPAL / MAIN FLOW ====
    Client->>+API: GET /places?page=1&limit=10&filters=wifi,pool
    API->>+Facade: getPlaces(filters, pagination)
    Facade->>+PlaceService: getPlaces(filters, pagination)
    
    PlaceService->>+PlaceRepo: findPlaces(criteria, pagination)
    PlaceRepo->>+DB: SELECT * FROM places WHERE ... LIMIT ? OFFSET ?
    DB-->>-PlaceRepo: places[]
    PlaceRepo-->>-PlaceService: places[]
    
    PlaceService->>+PlaceRepo: countTotal(criteria)
    PlaceRepo->>+DB: SELECT COUNT(*) FROM places WHERE ...
    DB-->>-PlaceRepo: totalCount
    PlaceRepo-->>-PlaceService: totalCount
    
    PlaceService->>PlaceService: buildPaginationResponse()
    PlaceService-->>-Facade: response
    Facade-->>-API: response
    API-->>-Client: 200 OK {places, pagination}

    %% ==== ERREUR ====
    alt Invalid parameters
        PlaceService-->>Facade: error INVALID_PARAMS
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 Bad Request
    end
```

 **FR :** Supporte la pagination, les filtres et le comptage total.  
 **EN :** Supports pagination, filters, and total count.

---

##  HTTP Codes – Codes de réponse

| Code | Signification (FR) | Meaning (EN) |
|------|-------------------|--------------|
| **200** | Requête GET réussie | Successful GET |
| **201** | Création réussie | Resource created |
| **400** | Données invalides | Invalid data |
| **401** | Non authentifié | Unauthorized |
| **403** | Action interdite | Forbidden |
| **404** | Ressource introuvable | Not found |
| **409** | Conflit (ex: email, review doublon) | Conflict (duplicate email/review) |
| **503** | Service temporairement indisponible | Service unavailable |

---

##  Concepts clés / Key Concepts

| Concept | FR | EN |
|---------|----|----|
| **Facade** | Point d'entrée unique vers la logique métier | Single entry point to business logic |
| **JWT** | Jeton d'authentification signé pour la sécurité | Signed authentication token |
| **Validation** | Email unique, prix ≥ 0, note 1–5, coordonnées valides | Unique email, price ≥ 0, rating 1–5, valid coordinates |
| **Règles métier / Business rules** | Pas d'auto-review, 1 avis par (utilisateur, lieu), mot de passe hashé | No self-review, 1 review per (user, place), password hashed |

---

##  Flux général / Global flow

```
Client  API  Auth (si requis)  Facade  Service  Repository  Database  (retour)
```

**FR :** Requête descend dans les couches, réponse remonte dans l'ordre inverse.  
**EN :** Request flows downward through layers, response flows back upward.