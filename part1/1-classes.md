# High-Level class Diagram (Task 1)
```mermaid
classDiagram
    class User {
        -String id (UUID)
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
    note for User "FR — Utilisateur :<br/>• email **unique** et au bon format (validateEmail).<br/>• password : **stocker un hash**, jamais le mot de passe en clair (hashPassword).<br/>• isAdmin : droits étendus (admin).<br/>• createdAt/updatedAt : gérés automatiquement.<br/>• Les règles (unicité, hash) sont appliquées côté service avant save.<br/><br/>EN — User:<br/>• email must be **unique** and valid (validateEmail).<br/>• password: **store a hash**, never plain text (hashPassword).<br/>• isAdmin: elevated privileges.<br/>• createdAt/updatedAt: auto-managed.<br/>• Service layer enforces uniqueness & hashing before save."

    class Place {
        -String id (UUID)
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
    note for Place "FR — Lieu :<br/>• price ≥ 0 (définir la monnaie/format).<br/>• latitude ∈ [-90..90], longitude ∈ [-180..180] (validateCoordinates).<br/>• Propriétaire lié via User→Place (voir relations).<br/>• calculateDistance : aide pour distance géo.<br/>• Timestamps automatiques.<br/><br/>EN — Place:<br/>• price ≥ 0 (currency/format TBD).<br/>• latitude in [-90..90], longitude in [-180..180] (validateCoordinates).<br/>• Owner linked through User→Place (see relations).<br/>• calculateDistance: geospatial helper.<br/>• Auto timestamps."

    class Review {
        -String id (UUID)
        -Integer rating
        -String comment
        -DateTime createdAt
        -DateTime updatedAt
        +createReview()
        +updateReview()
        +deleteReview()
        +validateRating()
    }
    note for Review "FR — Avis :<br/>• rating ∈ **[1..5]** (validateRating).<br/>• **Pas d’auto-review** : l’auteur ne peut pas noter sa propre annonce.<br/>• Optionnel : au plus 1 avis par couple (user, place).<br/>• Timestamps automatiques.<br/><br/>EN — Review:<br/>• rating ∈ **[1..5]** (validateRating).<br/>• **No self-review**: author cannot review their own place.<br/>• Optional: at most 1 review per (user, place).<br/>• Auto timestamps."

    class Amenity {
        -String id (UUID)
        -String name
        -String description
        -DateTime createdAt
        -DateTime updatedAt
        +createAmenity()
        +updateAmenity()
        +deleteAmenity()
    }
    note for Amenity "FR — Équipement :<br/>• name : idéalement **unique** et normalisé (casse/espaces).<br/>• description : optionnelle.<br/>• Utilisé en **N:N** avec Place (voir lien).<br/><br/>EN — Amenity:<br/>• name: ideally **unique** and normalized (case/whitespace).<br/>• description: optional.<br/>• Used in **M:N** with Place (see relation)."

    class UserService {
        +registerUser(userData)
        +loginUser(email, password)
        +getUserById(id)
        +updateUserProfile(id, data)
        +deleteUser(id)
        +getAllUsers()
    }
    note for UserService "FR — Service Utilisateur :<br/>• Applique : email unique, **hash du mot de passe**, validations.<br/>• loginUser : vérifie le mot de passe via le hash.<br/>• Pas d’accès SQL direct : passe par un Repository (couche persistance).<br/><br/>EN — User Service:<br/>• Enforces: unique email, **password hashing**, validations.<br/>• loginUser: verify password via hash check.<br/>• No direct SQL: always go through a Repository."

    class PlaceService {
        +createPlace(placeData, ownerId)
        +getPlaceById(id)
        +updatePlace(id, data, userId)
        +deletePlace(id, userId)
        +getPlacesByOwner(ownerId)
        +searchPlaces(criteria)
    }
    note for PlaceService "FR — Service Lieu :<br/>• Vérifie ownerId (seul le propriétaire peut modifier/supprimer).<br/>• Valide price et coordonnées.<br/>• searchPlaces : filtres (ville, prix, amenities) + **pagination** côté API.<br/><br/>EN — Place Service:<br/>• Validate ownerId (only owner can update/delete).<br/>• Validate price and coordinates.<br/>• searchPlaces: filters (city, price, amenities) + **pagination** at API level."

    class ReviewService {
        +createReview(reviewData, userId, placeId)
        +getReviewById(id)
        +updateReview(id, data, userId)
        +deleteReview(id, userId)
        +getReviewsByPlace(placeId)
        +getReviewsByUser(userId)
    }
    note for ReviewService "FR — Service Avis :<br/>• Valide rating (1..5) et **interdit l’auto-review** (user ≠ owner du place).<br/>• Peut imposer 1 avis par (user, place).<br/>• Contrôle auteur pour update/delete.<br/><br/>EN — Review Service:<br/>• Validate rating (1..5) and **deny self-review** (user ≠ place owner).<br/>• May enforce 1 review per (user, place).<br/>• Ensure author identity on update/delete."

    class AmenityService {
        +createAmenity(amenityData)
        +getAmenityById(id)
        +updateAmenity(id, data)
        +deleteAmenity(id)
        +getAllAmenities()
    }
    note for AmenityService "FR — Service Équipement :<br/>• Valide name (unicité, normalisation).<br/>• CRUD standard ; liaisons N:N avec Place gérées ailleurs (service/place ou facade).<br/><br/>EN — Amenity Service:<br/>• Validate name (uniqueness, normalization).<br/>• Standard CRUD; M:N linking with Place handled elsewhere (place service or facade)."

    %% Relationships
    User ||--o{ Place : owns
    User ||--o{ Review : writes
    Place ||--o{ Review : has
    Place }o--o{ Amenity : includes

    note for Place,User "FR — Relations clés :<br/>• User 1 — * Place (un utilisateur possède plusieurs lieux).<br/>• Place 1 — * Review (un lieu a plusieurs avis).<br/>• User 1 — * Review (un user peut écrire plusieurs avis).<br/>• Place * — * Amenity (N:N via table de jointure côté persistance).<br/><br/>EN — Key relations:<br/>• User 1 — * Place (a user owns many places).<br/>• Place 1 — * Review (a place has many reviews).<br/>• User 1 — * Review (a user can write many reviews).<br/>• Place * — * Amenity (M:N via join table in persistence)."

    UserService --> User : manages
    PlaceService --> Place : manages
    ReviewService --> Review : manages
    AmenityService --> Amenity : manages

    PlaceService --> User : validates_owner
    ReviewService --> User : validates_author
    ReviewService --> Place : validates_place

    %% Global legend (inside image)
    class Legend {
        <<legend>>
    }
    note for Legend "FR — Lecture :<br/>• Les **entités** (User, Place, Review, Amenity) sont stockées en base (UUID, timestamps, contraintes).<br/>• Les **Services** appliquent les règles (unicité email, hash, rating 1..5, no self-review, lat/lon valides, price≥0) et ne parlent pas SQL directement : ils passent par des **Repositories** (couche persistance, montrés dans le diagramme d’architecture).<br/><br/>EN — How to read:<br/>• **Entities** (User, Place, Review, Amenity) are persisted (UUID, timestamps, constraints).<br/>• **Services** enforce rules (unique email, hashing, rating 1..5, no self-review, valid lat/lon, price≥0) and never do raw SQL: they call **Repositories** (persistence layer, shown in the architecture diagram)."

