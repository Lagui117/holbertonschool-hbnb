# High-Level Package Diagram (Task 0)

## Architecture en Couches / Layered Architecture

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

---

##  Flux global / Global flow

**FR :**  
Le client envoie une requête  API / Endpoints  
Elle passe par la **Facade** (HBnB Facade)  
La Facade délègue au bon **Service** (User, Place, Review, Amenity)  
Le Service applique les règles et appelle un **Repository**  
Le Repository communique avec la **Database**  
La réponse remonte dans le sens inverse.

**EN :**  
Client sends request  API / Endpoints  
Goes through **HBnB Facade**  
Facade delegates to the correct **Service** (User, Place, Review, Amenity)  
Service applies rules and calls a **Repository**  
Repository interacts with **Database**  
Response flows back upward.

 **Sens unique** : Presentation  Business  Persistence (jamais l'inverse)  
 **One-way** : Presentation  Business  Persistence (never the other way)

---

##  Rôle des éléments / Role of components

| Élément | FR | EN |
|---------|----|----|
| **API / Endpoints** | Reçoivent les requêtes HTTP (GET, POST…) | Receive HTTP requests |
| **HBnB Facade** | Porte d'entrée unique vers la logique métier | Single entry point to business logic |
| **Services** | Appliquent les règles métiers (validation, sécurité…) | Enforce business rules (validation, security…) |
| **Models** | Représentent les entités principales (User, Place, Review, Amenity) | Represent domain entities |
| **Repositories** | Accès structuré aux données (CRUD) | Structured access to data (CRUD) |
| **Database** | Stocke toutes les entités de manière persistante | Stores all entities persistently |

---

##  Exemple concret / Example flow

**FR :**
```
POST /users  API  Facade  UserService  UserRepo  Database  Réponse 201
```

**EN :**
```
POST /users  API  Facade  UserService  UserRepo  Database  201 Created
```

---

##  Règles importantes / Key rules

###  À éviter / Avoid
- **Aucune logique métier dans la couche Presentation**  
  *No business logic in Presentation layer*
  
- **Aucune requête SQL directe dans les Services**  
  *No raw SQL in Services*

###  Bonnes pratiques / Best practices
- **Une seule entrée : la Facade**  
  *Single entry point: the Facade*
  
- **Les dépendances descendent seulement**  
  *Dependencies go downward only*

---

##  Résumé / Summary

**FR :**  
Ce diagramme illustre la structure modulaire et hiérarchique d'HBnB. Chaque couche a une responsabilité unique, garantissant clarté, testabilité et maintenabilité.

**EN :**  
This diagram shows HBnB's layered architecture. Each layer has a single responsibility, ensuring clarity, testability, and maintainability.

---

##  Concepts clés / Key concepts

### Pattern Facade
**FR :** Le facade sert de point d'entrée unique pour simplifier l'accès à la logique métier complexe. Il réduit le couplage entre la couche de présentation et les services métier.

**EN :** The facade acts as a single entry point to simplify access to complex business logic. It reduces coupling between the presentation layer and business services.

### Séparation des responsabilités / Separation of concerns
- **Presentation** : Gestion des requêtes/réponses HTTP
- **Business Logic** : Application des règles métier
- **Persistence** : Accès et gestion des données

### Avantages / Benefits
 **Maintenabilité** : Modifications isolées par couche  
 **Testabilité** : Chaque composant testable indépendamment  
 **Évolutivité** : Ajout de fonctionnalités sans régression  
 **Clarté** : Responsabilités bien définies