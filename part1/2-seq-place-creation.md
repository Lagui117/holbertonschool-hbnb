## High-Level Class Diagram (Task 2)

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

    Note over Client,DB: ARCHITECTURE OVERVIEW<br/>EN: API + Auth → Facade → Services → Repository → Database<br/>FR: API + Auth → Facade → Services → Repository → Base de données

    rect rgb(230, 240, 255)
        Note over Client,API: AUTHENTICATION PHASE / PHASE D'AUTHENTIFICATION
        Client->>+API: POST /places<br/>{title, description, price, lat, lng, amenities}
        Note right of API: EN: Parse JSON + validate required fields<br/>FR: Parser JSON + valider champs requis
        
        API->>+Auth: validateToken(Authorization: Bearer token)
        Note right of Auth: EN: Verify JWT signature & expiration<br/>FR: Vérifier signature JWT & expiration
        Auth->>Auth: verifyJWT(token)
        Auth->>Auth: extractUserId(token)
        Auth-->>-API: userId
        Note right of Auth: EN: Token valid → extract userId<br/>FR: Token valide → extraire userId
    end

    rect rgb(240, 255, 240)
        Note over API,PlaceService: BUSINESS LOGIC PHASE / PHASE LOGIQUE MÉTIER
        API->>+Facade: createPlace(placeData, userId)
        Note right of Facade: EN: Orchestrate services + standardize errors<br/>FR: Orchestrer services + standardiser erreurs
        
        Facade->>+PlaceService: createPlace(placeData, userId)
        
        PlaceService->>+UserService: getUserById(userId)
        Note right of UserService: EN: Verify user exists and is active<br/>FR: Vérifier utilisateur existe et est actif
        UserService-->>-PlaceService: user
        
        PlaceService->>PlaceService: validatePlaceData(placeData)
        Note right of PlaceService: EN: Check title not empty<br/>FR: Vérifier titre non vide
        
        PlaceService->>PlaceService: validateCoordinates(lat, lng)
        Note right of PlaceService: EN: lat ∈ [-90, 90] & lng ∈ [-180, 180]<br/>FR: lat ∈ [-90, 90] & lng ∈ [-180, 180]
        
        PlaceService->>PlaceService: validatePrice(price)
        Note right of PlaceService: EN: price ≥ 0<br/>FR: prix ≥ 0
        
        PlaceService->>PlaceService: validateAmenities(amenities)
        Note right of PlaceService: EN: Optional: check amenity IDs exist<br/>FR: Optionnel: vérifier IDs amenities existent
    end

    rect rgb(255, 245, 230)
        Note over PlaceService,DB: PERSISTENCE PHASE / PHASE PERSISTANCE
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
        
        PlaceRepo->>+DB: BEGIN TRANSACTION
        PlaceRepo->>DB: INSERT INTO places VALUES(...)
        PlaceRepo->>DB: COMMIT
        DB-->>-PlaceRepo: success
        
        PlaceRepo-->>-PlaceService: savedPlace
        
        PlaceService->>PlaceService: sanitize(savedPlace)
        Note right of PlaceService: EN: Remove internal/sensitive fields<br/>FR: Retirer champs internes/sensibles
        
        PlaceService-->>-Facade: sanitizedPlace
        Facade-->>-API: sanitizedPlace
        API-->>-Client: 201 Created<br/>{id, title, price, owner, createdAt}
    end

    Note over Client,DB: ERROR SCENARIOS / SCÉNARIOS D'ERREUR

    alt Invalid/Missing JWT
        Auth-->>API: error INVALID_TOKEN
        API-->>Client: 401 Unauthorized<br/>{"error":"INVALID_TOKEN"}
        Note right of Auth: EN: Token missing, expired or invalid signature<br/>FR: Token absent, expiré ou signature invalide
        
    else User Not Found
        UserService-->>PlaceService: null
        PlaceService-->>Facade: error USER_NOT_FOUND
        Facade-->>API: 404 Not Found
        API-->>Client: 404 {"error":"USER_NOT_FOUND"}
        Note right of UserService: EN: Owner does not exist<br/>FR: Propriétaire n'existe pas
        
    else Invalid Coordinates
        PlaceService-->>Facade: error INVALID_COORDINATES
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_COORDINATES"}
        Note right of PlaceService: EN: Latitude or longitude out of range<br/>FR: Latitude ou longitude hors limites
        
    else Invalid Price
        PlaceService-->>Facade: error INVALID_PRICE
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_PRICE"}
        Note right of PlaceService: EN: Price must be ≥ 0<br/>FR: Prix doit être ≥ 0
        
    else Invalid Amenities
        PlaceService-->>Facade: error INVALID_AMENITIES
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_AMENITIES"}
        Note right of PlaceService: EN: Unknown amenity IDs<br/>FR: IDs d'amenities inconnus
        
    else Database Unavailable
        DB-->>PlaceRepo: CONNECTION_TIMEOUT
        PlaceRepo-->>PlaceService: dbError timeout
        PlaceService-->>Facade: error STORAGE_ERROR
        Facade-->>API: 503 Service Unavailable
        API-->>Client: 503 {"error":"STORAGE_ERROR"}
        Note right of DB: EN: DB down or timeout<br/>FR: DB indisponible ou timeout
    end

    Note over Client,DB: CONCEPTS CLÉS (FR)<br/>JWT: Jeton signé prouvant identité sans requête DB<br/>Auth Middleware: Filtre validant JWT avant logique métier<br/>Facade: Point entrée unique orchestrant services<br/>Service: Applique règles métier (validations, permissions)<br/>Repository: Interface accès données (masque SQL)<br/>Transaction: Opération atomique (tout ou rien)<br/>Sanitization: Retrait champs internes/sensibles<br/>UUID v4: Identifiant unique universel<br/>Validation: title requis, price≥0, lat[-90,90], lng[-180,180]
