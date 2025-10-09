# High-Level Package Diagram (Task 0)

```mermaid
graph TB
    %% ============= LAYERS =============
    subgraph "Presentation Layer"
        API[API Controllers]
        Endpoints[REST Endpoints]
        Services[Web Services]
    end
    
    subgraph "Business Logic Layer"
        Facade[HBnB Facade]
        UserService[User Service]
        PlaceService[Place Service]
        ReviewService[Review Service]
        AmenityService[Amenity Service]
        Models[Domain Models]
    end
    
    subgraph "Persistence Layer"
        UserRepo[User Repository]
        PlaceRepo[Place Repository]
        ReviewRepo[Review Repository]
        AmenityRepo[Amenity Repository]
        Database[(Database)]
    end
    
    %% ============= FLOWS =============
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

    %% ============= EMBEDDED LEGEND =============
    subgraph Legend["Legend / Légende (integrated)"]
        LFR["FR — En bref :
- Presentation (= salle/serveur) reçoit la requête.
- Ça passe par **HBnB Facade** (porte d’entrée métier).
- La Facade délègue à un **Service** (User/Place/Review/Amenity) qui applique les règles et manipule les **Models**.
- Pour lire/écrire, le Service passe par un **Repository** jusqu’à la **Database**.
- Retour : Database → Repository → Service → Facade → API → Client.
Idée clé : sens unique **Presentation → Business → Persistence** (jamais l’inverse)."]
        LEN["EN — In short:
- Presentation (dining room/waiter) receives the request.
- It goes through **HBnB Facade** (single business entry point).
- The Facade delegates to a **Service** (User/Place/Review/Amenity) that applies rules and uses **Models**.
- Read/write goes via a **Repository** down to the **Database**.
- Back path: Database → Repository → Service → Facade → API → Client.
Key idea: one-way **Presentation → Business → Persistence** (never the other way)."]
    end

    %% ============= STYLES =============
    classDef presentationLayer fill:#e1f5fe,stroke:#90caf9,color:#0d47a1
    classDef businessLayer fill:#f3e5f5,stroke:#ce93d8,color:#4a148c
    classDef persistenceLayer fill:#e8f5e9,stroke:#81c784,color:#1b5e20
    classDef legendStyle fill:#f9f9f9,stroke:#cfcfcf,color:#333

    class API,Endpoints,Services presentationLayer
    class Facade,UserService,PlaceService,ReviewService,AmenityService,Models businessLayer
    class UserRepo,PlaceRepo,ReviewRepo,AmenityRepo,Database persistenceLayer
    class LFR,LEN legendStyle
'''
🎯 Flux global / Global flow


FR :

Le client envoie une requête → API / Endpoints

Elle passe par la Facade (HBnB Facade)

La Facade délègue au bon Service (User, Place, Review, Amenity)

Le Service applique les règles et appelle un Repository

Le Repository communique avec la Database

La réponse remonte dans le sens inverse.

EN :

Client sends request → API / Endpoints

Goes through HBnB Facade

Facade delegates to the correct Service

Service applies rules and calls a Repository

Repository interacts with Database

Response flows back upward.

➡️ Sens unique : Presentation → Business → Persistence (jamais l’inverse)

🧩 Rôle des éléments / Role of components
Élément	FR	EN
API / Endpoints	Reçoivent les requêtes HTTP (GET, POST…).	Receive HTTP requests.
HBnB Facade	Porte d’entrée unique vers la logique métier.	Single entry point to business logic.
Services	Appliquent les règles métiers (validation, sécurité…).	Enforce business rules (validation, security…).
Models	Représentent les entités principales (User, Place, Review, Amenity).	Represent domain entities.
Repositories	Accès structuré aux données (CRUD).	Structured access to data (CRUD).
Database	Stocke toutes les entités de manière persistante.	Stores all entities persistently.
💡 Exemple concret / Example flow
```
FR :
POST /users → API → Facade → UserService → UserRepo → Database → Réponse 201.

EN :
POST /users → API → Facade → UserService → UserRepo → Database → 201 Created.

🧱 Règles importantes / Key rules

❌ Aucune logique métier dans la couche Presentation
(No business logic in Presentation layer)

❌ Aucune requête SQL directe dans les Services
(No raw SQL in Services)

✅ Une seule entrée : la Facade
(Single entry point: the Facade)

✅ Les dépendances descendent seulement
(Dependencies go downward only)

🧾 Résumé / Summary

FR :
Ce diagramme illustre la structure modulaire et hiérarchique d’HBnB. Chaque couche a une responsabilité unique, garantissant clarté, testabilité et maintenabilité.

EN :
This diagram shows HBnB’s layered architecture. Each layer has a single responsibility, ensuring clarity, testability, and maintainability.