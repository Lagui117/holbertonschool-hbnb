sequenceDiagram
    autonumber
    participant Client
    participant API as API Controller
    participant Facade as HBnB Facade
    participant UserService as User Service
    participant User as User Model
    participant UserRepo as User Repository
    participant DB as Database

    Note over Client,DB: CONTEXT / CONTEXTE<br/>EN: Presentation (API) → Business (Facade+Service) → Persistence (Repo+DB)<br/>FR: Présentation (API) → Métier (Facade+Service) → Persistance (Repo+DB)

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
        Note right of API: EN: Uniqueness violation<br/>FR: Violation d'unicité
        
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
        Note over UserRepo,DB: EN: Two concurrent requests<br/>FR: Deux requêtes simultanées
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

    Note over Client,DB: DEFINITIONS (FR)<br/>Facade: Point entrée unique vers logique métier<br/>Service: Applique règles métier, pas de SQL<br/>Repository: Interface accès données<br/>Entity: Objet domaine avec UUID + timestamps<br/>Hash: Transformation irréversible (bcrypt/argon2)<br/>Sanitization: Retrait champs sensibles<br/>Transaction: Bloc atomique (tout ou rien)<br/>Race condition: Conflit requêtes simultanées<br/>UUID v4: Identifiant unique (128 bits)<br/>Normalisation: trim + lowercase email
