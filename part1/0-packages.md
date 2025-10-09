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

    %% ============= STYLES (simple, compatibles) =============
    classDef presentationLayer fill:#e1f5fe,stroke:#90caf9,color:#0d47a1
    classDef businessLayer fill:#f3e5f5,stroke:#ce93d8,color:#4a148c
    classDef persistenceLayer fill:#e8f5e9,stroke:#81c784,color:#1b5e20

    class API,Endpoints,Services presentationLayer
    class Facade,UserService,PlaceService,ReviewService,AmenityService,Models businessLayer
    class UserRepo,PlaceRepo,ReviewRepo,AmenityRepo,Database persistenceLayer
```

### 🎯 Flux global / Global flow
**FR :**  
Client → API/Endpoints → **Facade** → Service (User/Place/Review/Amenity) → Repository → Database → retour.  
Sens unique : **Presentation → Business → Persistence**.

**EN :**  
Client → API/Endpoints → **Facade** → Service (User/Place/Review/Amenity) → Repository → Database → back.  
One-way : **Presentation → Business → Persistence**.

### 🧩 Rôle des éléments / Role of components
- **API / Endpoints** — FR: reçoivent les requêtes HTTP. EN: receive HTTP requests.  
- **HBnB Facade** — FR: porte d’entrée unique métier. EN: single business entry point.  
- **Services** — FR: appliquent les règles métier. EN: enforce business rules.  
- **Models** — FR: entités du domaine (User, Place, Review, Amenity). EN: domain entities.  
- **Repositories** — FR: accès données structuré (CRUD). EN: structured data access (CRUD).  
- **Database** — FR/EN: stockage persistant.

### ✅ Règles clés / Key rules
- ❌ Pas de logique métier dans **Presentation** / No business logic in Presentation  
- ❌ Pas de SQL direct dans **Services** / No raw SQL in Services  
- ✅ Passer par la **Facade** / Use the Facade  
- ✅ Dépendances descendantes uniquement / Dependencies go downward only
