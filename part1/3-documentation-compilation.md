# HBnB Evolution - Complete Technical Documentation / Documentation Technique Complète

##  Project Information / Informations du Projet

**Project / Projet :** HBnB Evolution - Part 1 (UML Design)  
**Team / Équipe :** Yassin Jaghmim, Guillaume Watelet  
**Date :** October / Octobre 2025  
**Version :** 1.0  

---

##  Table of Contents / Table des matières

1. [Introduction](#introduction)
2. [General Architecture (Task 0) / Architecture Générale](#task-0-general-architecture--architecture-générale)
3. [Class Model (Task 1) / Modèle de Classes](#task-1-class-model--modèle-de-classes)
4. [Sequence Diagrams (Task 2) / Diagrammes de Séquence](#task-2-sequence-diagrams--diagrammes-de-séquence)
5. [Business Rules and Validation / Règles Métier et Validation](#business-rules-and-validation--règles-métier-et-validation)
6. [Conclusion](#conclusion)

---

## Introduction

###  Project Objective / Objectif du Projet

**EN:** HBnB Evolution is a simplified AirBnB-like application. This first part (Part 1) focuses on the **design and technical documentation** of the system architecture, without code implementation.

**FR:** HBnB Evolution est une application de type AirBnB simplifiée. Cette première partie (Part 1) se concentre sur la **conception et la documentation technique** de l'architecture du système, sans implémentation de code.

###  Deliverables / Livrables

**EN:** This documentation includes:
- **Package diagram** (layered architecture)
- **Class diagram** (entities and services)
- **4 sequence diagrams** (API flows)
- **Business rules and constraints**

**FR:** Cette documentation regroupe :
- **Diagramme de packages** (architecture en couches)
- **Diagramme de classes** (entités et services)
- **4 diagrammes de séquence** (flux API)
- **Règles métier et contraintes**

###  Architecture / Architecture Choisie

**Architectural Pattern / Pattern Architectural :** Layered Architecture / Architecture en couches  
**Design Pattern / Pattern de Conception :** Facade for inter-layer communication / Facade pour la communication entre couches

---

## Task 0: General Architecture / Architecture Générale

### Package Diagram - Overview / Diagramme de Packages - Vue d'ensemble

```mermaid
graph TB
    subgraph Presentation["Presentation Layer"]
        API[API Controllers]
        Endpoints[REST Endpoints]
        Services[Web Services]
    end
    
    subgraph Business["Business Logic Layer"]
        Facade[HBnB Facade]
        UserService[User Service]
        PlaceService[Place Service]
        ReviewService[Review Service]
        AmenityService[Amenity Service]
        Models[Domain Models]
    end
    
    subgraph Persistence["Persistence Layer"]
        UserRepo[User Repository]
        PlaceRepo[Place Repository]
        ReviewRepo[Review Repository]
        AmenityRepo[Amenity Repository]
        Database[(Database)]
    end
    
    API --> Facade
    Endpoints --> Facade
    Services --> Facade
    
    Facade --> UserService
    Facade --> PlaceService
    Facade --> ReviewService
    Facade --> AmenityService
    
    UserService --> Models
    PlaceService --> Models
    ReviewService --> Models
    AmenityService --> Models
    
    UserService --> UserRepo
    PlaceService --> PlaceRepo
    ReviewService --> ReviewRepo
    AmenityService --> AmenityRepo
    
    UserRepo --> Database
    PlaceRepo --> Database
    ReviewRepo --> Database
    AmenityRepo --> Database
    
    classDef presentationLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef businessLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef persistenceLayer fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class API,Endpoints,Services presentationLayer
    class Facade,UserService,PlaceService,ReviewService,AmenityService,Models businessLayer
    class UserRepo,PlaceRepo,ReviewRepo,AmenityRepo,Database persistenceLayer
```

###  Communication Flow / Flux de Communication

```
Client  API  Facade  Service  Repository  Database  (back)
Client  API  Facade  Service  Repository  Database  (retour)
```

**EN:** Request flows downward through layers, response flows back upward.  
**FR:** Requête descend dans les couches, réponse remonte dans l'ordre inverse.

###  Layer Responsibilities / Rôle des Couches

| Layer / Couche | Responsibility (EN) | Responsabilité (FR) |
|----------------|---------------------|---------------------|
| **Presentation** | Handles HTTP requests, JSON parsing, basic validation | Gestion des requêtes HTTP, parsing JSON, validation basique |
| **Business Logic** | Enforces business rules, orchestration, validation | Application des règles métier, orchestration, validation |
| **Persistence** | Data access, transactions, database communication | Accès aux données, transactions, communication base de données |

###  Facade Pattern

**EN:** The Facade acts as a **single entry point** to business logic. It simplifies interactions between presentation and business services, reduces coupling, and standardizes error handling.

**FR:** Le Facade sert de **point d'entrée unique** vers la logique métier. Il simplifie les interactions entre la couche de présentation et les services métier, réduit le couplage et standardise la gestion des erreurs.

**Benefits / Avantages :**
-  Reduces coupling between layers / Réduit le couplage entre couches
-  Centralizes orchestration / Centralise l'orchestration
-  Facilitates unit testing / Facilite les tests unitaires
-  Standardizes error handling / Standardise la gestion des erreurs

---

## Task 1: Class Model / Modèle de Classes

### Complete Class Diagram / Diagramme de Classes Complet

```mermaid
classDiagram
    class User {
        -String id
        -String firstName
        -String lastName
        -String email
        -String password
        -Boolean isAdmin
        -DateTime createdAt
        -DateTime updatedAt
        +createUser()
        +updateUser()
        +deleteUser()
        +validateEmail()
        +hashPassword()
    }
    
    class Place {
        -String id
        -String title
        -String description
        -Float price
        -Float latitude
        -Float longitude
        -DateTime createdAt
        -DateTime updatedAt
        +createPlace()
        +updatePlace()
        +deletePlace()
        +validateCoordinates()
        +calculateDistance()
    }
    
    class Review {
        -String id
        -Integer rating
        -String comment
        -DateTime createdAt
        -DateTime updatedAt
        +createReview()
        +updateReview()
        +deleteReview()
        +validateRating()
    }
    
    class Amenity {
        -String id
        -String name
        -String description
        -DateTime createdAt
        -DateTime updatedAt
        +createAmenity()
        +updateAmenity()
        +deleteAmenity()
    }
    
    class UserService {
        +registerUser(userData)
        +loginUser(email, password)
        +getUserById(id)
        +updateUserProfile(id, data)
        +deleteUser(id)
        +getAllUsers()
    }
    
    class PlaceService {
        +createPlace(placeData, ownerId)
        +getPlaceById(id)
        +updatePlace(id, data, userId)
        +deletePlace(id, userId)
        +getPlacesByOwner(ownerId)
        +searchPlaces(criteria)
    }
    
    class ReviewService {
        +createReview(reviewData, userId, placeId)
        +getReviewById(id)
        +updateReview(id, data, userId)
        +deleteReview(id, userId)
        +getReviewsByPlace(placeId)
        +getReviewsByUser(userId)
    }
    
    class AmenityService {
        +createAmenity(amenityData)
        +getAmenityById(id)
        +updateAmenity(id, data)
        +deleteAmenity(id)
        +getAllAmenities()
    }
    
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has
    Place "0..*" --> "0..*" Amenity : includes
    
    UserService ..> User : manages
    PlaceService ..> Place : manages
    ReviewService ..> Review : manages
    AmenityService ..> Amenity : manages
    
    PlaceService ..> User : validates_owner
    ReviewService ..> User : validates_author
    ReviewService ..> Place : validates_place
```

###  Domain Entities / Entités du Domaine

####  User / Utilisateur

**EN:**
- Represents a registered user in the system
- `id`: Unique identifier (UUID v4)
- `email`: Must be unique and valid
- `password`: Stored as hash (never plain text)
- `isAdmin`: Boolean for elevated privileges
- `createdAt/updatedAt`: Automatic timestamps for auditing

**FR:**
- Représente un utilisateur enregistré dans le système
- `id`: Identifiant unique (UUID v4)
- `email`: Doit être unique et valide
- `password`: Stocké sous forme de hash (jamais en clair)
- `isAdmin`: Booléen pour privilèges élevés
- `createdAt/updatedAt`: Timestamps automatiques pour l'audit

####  Place / Lieu

**EN:**
- Represents a place listed by a user
- `price`: Must be ≥ 0
- `latitude`: Must be in [-90, 90]
- `longitude`: Must be in [-180, 180]
- Methods validate coordinates and calculate distances

**FR:**
- Représente un lieu publié par un utilisateur
- `price`: Doit être ≥ 0
- `latitude`: Doit être dans [-90, 90]
- `longitude`: Doit être dans [-180, 180]
- Méthodes pour valider coordonnées et calculer distances

####  Review / Avis

**EN:**
- Represents a review left by a user on a place
- `rating`: Integer between 1 and 5
- **Business rules:**
  - User cannot review their own place
  - One review per user per place

**FR:**
- Représente un avis laissé par un utilisateur sur un lieu
- `rating`: Entier entre 1 et 5
- **Règles métier:**
  - Utilisateur ne peut pas noter son propre lieu
  - Un avis par utilisateur par lieu

####  Amenity / Commodité

**EN:**
- Represents an amenity or service (WiFi, pool, parking)
- Many-to-many relationship with Place
- Names should be unique and normalized

**FR:**
- Représente une commodité ou service (WiFi, piscine, parking)
- Relation plusieurs-à-plusieurs avec Place
- Noms doivent être uniques et normalisés

###  Relationships / Relations

| Relation | Cardinality / Cardinalité | Description (EN) | Description (FR) |
|----------|---------------------------|------------------|------------------|
| **User  Place** | `1 : 0..*` | One user owns zero or more places | Un utilisateur possède zéro ou plusieurs lieux |
| **User  Review** | `1 : 0..*` | One user writes zero or more reviews | Un utilisateur écrit zéro ou plusieurs avis |
| **Place  Review** | `1 : 0..*` | One place has zero or more reviews | Un lieu contient zéro ou plusieurs avis |
| **Place  Amenity** | `0..* : 0..*` | Many-to-many relationship | Relation plusieurs-à-plusieurs |

---

## Task 2: Sequence Diagrams / Diagrammes de Séquence

### 1⃣ User Registration / Inscription utilisateur

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
    UserRepo->>+DB: SELECT * FROM users WHERE email = ?
    DB-->>-UserRepo: null
    UserRepo-->>-UserService: null
    
    UserService->>UserService: createUser(userData)
    UserService->>+UserRepo: save(user)
    UserRepo->>+DB: INSERT INTO users VALUES (...)
    DB-->>-UserRepo: success
    UserRepo-->>-UserService: savedUser
    
    UserService-->>-Facade: sanitizedUser
    Facade-->>-API: sanitizedUser
    API-->>-Client: 201 Created

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

 **EN:** Checks unique email, hashes password before saving.  
 **FR:** Vérifie l'unicité de l'email, hache le mot de passe avant stockage.

---

### 2⃣ Place Creation / Création de lieu

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
    
    PlaceService->>+PlaceRepo: save(place)
    PlaceRepo->>+DB: INSERT INTO places VALUES (...)
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

 **EN:** JWT required, valid coordinates, price ≥ 0.  
 **FR:** JWT requis, coordonnées valides, prix ≥ 0.

---

### 3⃣ Review Submission / Soumission d'avis

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

 **EN:** User cannot review their own place, one review per place only.  
 **FR:** Un utilisateur ne peut pas noter son propre lieu, un seul avis par lieu.

---

### 4⃣ Fetch Places List / Récupération de la liste des lieux

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API
    participant Facade
    participant PlaceService
    participant PlaceRepo
    participant DB

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

    alt Invalid parameters
        PlaceService-->>Facade: error INVALID_PARAMS
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 Bad Request
    end
```

 **EN:** Supports pagination, filters, and total count.  
 **FR:** Supporte la pagination, les filtres et le comptage total.

---

## Business Rules and Validation / Règles Métier et Validation

###  Global Validation Rules / Règles de Validation Globales

| Rule / Règle | EN | FR |
|--------------|----|----|
| **Unique IDs** | All objects use UUID v4 | Tous les objets utilisent UUID v4 |
| **Audit trail** | createdAt and updatedAt mandatory | createdAt et updatedAt obligatoires |
| **Unique email** | Verified at service and database level | Vérifié au niveau service et base de données |
| **No self-review** | User cannot review their own place | Utilisateur ne peut pas noter son propre lieu |
| **One review per place** | One review per user per place | Un avis par utilisateur par lieu |
| **Valid coordinates** | lat ∈ [-90, 90], lng ∈ [-180, 180] | lat ∈ [-90, 90], lng ∈ [-180, 180] |
| **Positive price** | price ≥ 0 | prix ≥ 0 |
| **Valid rating** | rating ∈ [1, 5] | rating ∈ [1, 5] |
| **Password security** | Hashed with bcrypt/argon2 (never plain text) | Hashé avec bcrypt/argon2 (jamais en clair) |

###  HTTP Status Codes / Codes de Statut HTTP

| Code | Meaning (EN) | Signification (FR) |
|------|--------------|-------------------|
| **200** | Successful GET | Requête GET réussie |
| **201** | Resource created | Ressource créée |
| **400** | Invalid data | Données invalides |
| **401** | Unauthorized | Non authentifié |
| **403** | Forbidden | Action interdite |
| **404** | Not found | Ressource introuvable |
| **409** | Conflict (duplicate email/review) | Conflit (email/avis dupliqué) |
| **503** | Service unavailable | Service indisponible |

###  Key Technical Concepts / Concepts Techniques Clés

| Concept | EN | FR |
|---------|----|----|
| **Facade** | Single entry point to business logic | Point d'entrée unique vers la logique métier |
| **JWT** | Signed authentication token | Jeton d'authentification signé |
| **Validation** | Unique email, price ≥ 0, rating 1-5, valid coordinates | Email unique, prix ≥ 0, note 1-5, coordonnées valides |
| **Business rules** | No self-review, 1 review per (user, place), password hashed | Pas d'auto-review, 1 avis par (utilisateur, lieu), mot de passe hashé |
| **Repository** | Data access abstraction layer | Couche d'abstraction d'accès aux données |
| **Service** | Business logic implementation | Implémentation de la logique métier |

---

## Conclusion

###  Summary / Résumé

**EN:**  
This document presents the complete UML design for HBnB Evolution Part 1. The layered architecture with Facade pattern ensures:
- Clear separation of concerns
- Easy testability and maintainability
- Scalability for future features
- Standardized error handling

The design follows SOLID principles and industry best practices, providing a solid foundation for implementation in Part 2.

**FR:**  
Ce document présente la conception UML complète pour HBnB Evolution Part 1. L'architecture en couches avec pattern Facade garantit :
- Séparation claire des responsabilités
- Testabilité et maintenabilité facilitées
- Évolutivité pour les fonctionnalités futures
- Gestion standardisée des erreurs

La conception suit les principes SOLID et les meilleures pratiques de l'industrie, fournissant une base solide pour l'implémentation dans la Part 2.

###  Next Steps / Prochaines Étapes

1. **Part 2:** REST API implementation / Implémentation de l'API REST
2. **Part 3:** Database integration / Intégration de la base de données
3. **Part 4:** Frontend interface / Interface utilisateur frontend

###  Team / Équipe

- **Yassin Jaghmim**
- **Guillaume Watelet**

**Date:** October 2025 / Octobre 2025  
**Version:** 1.0  
**Status:** Ready for review / Prêt pour revue
