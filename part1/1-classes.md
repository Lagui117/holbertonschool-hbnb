## High-Level Class Diagram (Task 1)

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
note for User "
FR: Utilisateur.
- email unique et format valide (validateEmail)
- password: stocker un hash (hashPassword)
- isAdmin: droits etendus
- createdAt/updatedAt: automatiques
EN: User.
- email must be unique and valid
- password: store a hash
- isAdmin: elevated rights
- timestamps auto-managed
"

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
note for Place "
FR: Lieu.
- price >= 0
- latitude in [-90..90], longitude in [-180..180]
- proprietaire via User->Place
- calculateDistance: utilitaire geo
EN: Place.
- price >= 0
- lat in [-90..90], lon in [-180..180]
- owner via User->Place
- calculateDistance: geo helper
"

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
note for Review "
FR: Avis.
- rating in [1..5]
- pas d'auto-review (auteur != proprietaire)
- option: 1 avis par (user, place)
EN: Review.
- rating in [1..5]
- no self-review (author != owner)
- optional: at most 1 per (user, place)
"

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
note for Amenity "
FR: Equipement.
- name idealement unique et normalise
- M:N avec Place
EN: Amenity.
- name ideally unique/normalized
- M:N with Place
"

class UserService {
    +registerUser(userData)
    +loginUser(email, password)
    +getUserById(id)
    +updateUserProfile(id, data)
    +deleteUser(id)
    +getAllUsers()
}
note for UserService "
FR: Service Utilisateur.
- applique: email unique, hash password
- login: verifie le hash
- pas de SQL direct (via repo)
EN: User Service.
- enforces unique email, hashing
- login checks hash
- no raw SQL (via repo)
"

class PlaceService {
    +createPlace(placeData, ownerId)
    +getPlaceById(id)
    +updatePlace(id, data, userId)
    +deletePlace(id, userId)
    +getPlacesByOwner(ownerId)
    +searchPlaces(criteria)
}
note for PlaceService "
FR: Service Lieu.
- verifie owner pour update/delete
- valide price et coordonnees
- search: filtres + pagination
EN: Place Service.
- validates owner for update/delete
- validates price and coords
- search: filters + pagination
"

class ReviewService {
    +createReview(reviewData, userId, placeId)
    +getReviewById(id)
    +updateReview(id, data, userId)
    +deleteReview(id, userId)
    +getReviewsByPlace(placeId)
    +getReviewsByUser(userId)
}
note for ReviewService "
FR: Service Avis.
- rating [1..5], pas d'auto-review
- au plus 1 avis par (user, place)
- controle auteur pour update/delete
EN: Review Service.
- rating [1..5], no self-review
- at most 1 per (user, place)
- author check on update/delete
"

class AmenityService {
    +createAmenity(amenityData)
    +getAmenityById(id)
    +updateAmenity(id, data)
    +deleteAmenity(id)
    +getAllAmenities()
}
note for AmenityService "
FR: Service Equipement.
- valide nom (unicite, normalisation)
- CRUD standard
EN: Amenity Service.
- validate name (unique/normalized)
- standard CRUD
"

%% Relationships
User ||--o{ Place : owns
User ||--o{ Review : writes
Place ||--o{ Review : has
Place }o--o{ Amenity : includes

UserService --> User : manages
PlaceService --> Place : manages
ReviewService --> Review : manages
AmenityService --> Amenity : manages

PlaceService --> User : validates_owner
ReviewService --> User : validates_author
ReviewService --> Place : validates_place
```