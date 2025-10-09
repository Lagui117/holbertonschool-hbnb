sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Facade as HBnB Facade
    participant PlaceService as Place Service
    participant PlaceRepo as Place Repository
    participant AmenityRepo as Amenity Repository
    participant DB as Database

    Note over Client,DB: EN: Public endpoint - List places with filters + pagination<br/>FR: Endpoint public - Lister lieux avec filtres + pagination

    Client->>+API: GET /places?page=1&limit=10&amenities=wifi,pool
    Note right of API: EN: Parse query params (page, limit, amenities)<br/>FR: Parser paramètres query (page, limit, amenities)
    
    API->>API: parseQueryParameters(query)
    Note right of API: EN: Set defaults, enforce max limit<br/>FR: Définir valeurs défaut, limite max
    
    API->>+Facade: getPlaces(filters, pagination)
    Note right of Facade: EN: Single entry point<br/>FR: Point entrée unique
    Facade->>+PlaceService: getPlaces(filters, pagination)
    
    PlaceService->>PlaceService: validateFilters(filters)
    Note right of PlaceService: EN: Validate price>=0, geo bounds, amenity slugs<br/>FR: Valider prix>=0, bornes géo, slugs amenities
    
    PlaceService->>PlaceService: buildSearchCriteria(filters)
    Note right of PlaceService: EN: Translate filters to DB criteria<br/>FR: Traduire filtres en critères DB
    
    PlaceService->>+PlaceRepo: findPlaces(criteria, pagination)
    Note right of PlaceRepo: EN: Apply LIMIT and OFFSET<br/>FR: Appliquer LIMIT et OFFSET
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
    Note right of PlaceService: EN: N+1 problem - consider batch fetch<br/>FR: Problème N+1 - envisager batch fetch
    
    PlaceService->>+PlaceRepo: countTotalPlaces(criteria)
    Note right of PlaceRepo: EN: Separate COUNT for pagination metadata<br/>FR: COUNT séparé pour métadonnées pagination
    
    PlaceRepo->>+DB: SELECT COUNT(*) FROM places WHERE ...
    DB-->>-PlaceRepo: totalCount
    PlaceRepo-->>-PlaceService: totalCount
    
    PlaceService->>PlaceService: buildPaginationResponse(places, totalCount, pagination)
    Note right of PlaceService: EN: Calculate page, limit, total, totalPages<br/>FR: Calculer page, limit, total, totalPages
    PlaceService-->>-Facade: paginatedResponse
    Facade-->>-API: paginatedResponse
    API-->>-Client: 200 OK {items:[], pagination:{page, limit, total, totalPages}}
    
    alt Invalid Pagination
        PlaceService-->>Facade: error INVALID_PAGINATION
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_PAGINATION"}
        Note right of API: EN: page or limit out of bounds<br/>FR: page ou limit hors limites
        
    else Invalid Filters
        PlaceService-->>Facade: error INVALID_FILTERS
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_FILTERS"}
        Note right of PlaceService: EN: Filter values invalid<br/>FR: Valeurs filtres invalides
        
    else Unknown Amenities
        PlaceService-->>Facade: error INVALID_AMENITIES
        Facade-->>API: 400 Bad Request
        API-->>Client: 400 {"error":"INVALID_AMENITIES"}
        Note right of AmenityRepo: EN: Amenity slugs/IDs not found<br/>FR: Slugs/IDs amenities introuvables
        
    else Database Error
        PlaceRepo-->>PlaceService: dbError timeout
        PlaceService-->>Facade: error STORAGE_ERROR
        Facade-->>API: 503 Service Unavailable
        API-->>Client: 503 {"error":"STORAGE_ERROR"}
        Note right of DB: EN: DB unavailable or timeout<br/>FR: DB indisponible ou timeout
    end
    
    Note over Client,DB: DEFINITIONS FR<br/>Pagination: LIMIT=taille, OFFSET=(page-1)*limit<br/>N+1: Chaque lieu = requête amenities<br/>Solution: Batch fetch ou JOIN<br/>Validation: prix>=0, page>0, limit max<br/>Codes: 400 invalide, 503 DB down
