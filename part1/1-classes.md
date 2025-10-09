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
note for User "FR: Utilisateur.\n- email unique et format valide (validateEmail)\n- password: stocker un hash (hashPassword)\n- isAdmin: droits etendus\n- createdAt/updatedAt: automatiques\nEN: User.\n- email must be unique and valid\n- password: store a hash\n- isAdmin: elevated rights\n- timestamps auto-managed"

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
note for Place "FR: Lieu.\n- price >= 0\n- latitude in [-90..90], longitude in [-180..180]\n- proprietaire via User->Place\n- calculateDistance: utilitaire geo\nEN: Place.\n- price >= 0\n- lat in [-90..90], lon in [-180..180]\n- owner via User->Place\n- calculateDistance: geo helper"

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
note for Review "FR: Avis.\n- rating in [1..5]\n- pas d'auto-review (auteur != proprietaire)\n- option: 1 avis par (user, place)\nEN: Review.\n- rating in [1..5]\n- no self-review (author != owner)\n- optional: at most 1 per (user, place)"

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
note for Amenity "FR: Equipement.\n- name idealement unique et normalise\n- M:N avec Place\nEN: Amenity.\n- name ideally unique/normalized\n- M:N with Place"

class UserService {
    +registerUser(userData)
    +loginUser(email, password)
    +getUserById(id)
    +updateUserProfile(id, data)
    +deleteUser(id)
    +getAllUsers()
}
note for UserService "FR: Service Utilisateur.\n- applique: email unique, hash password\n- login: verifie le hash\n- pas de SQL direct (via repo)\nEN: User Service.\n- enforces unique email, hashing\n- login checks hash\n- no raw SQL (via repo)"

class PlaceService {
    +createPlace(placeData, ownerId)
    +getPlaceById(id)
    +updatePlace(id, data, userId)
    +deletePlace(id, userId)
    +getPlacesByOwner(ownerId)
    +searchPlaces(criteria)
}
note for PlaceService "FR: Service Lieu.\n- verifie owner pour update/delete\n- valide price et coordonnees\n- search: filtres + pagination\nEN: Place Service.\n- validates owner for update/delete\n- validates price and coords\n- search: filters + pagination"

class ReviewService {
    +createReview(reviewData, userId, placeId)
    +getReviewById(id)
    +updateReview(id, data, userId)
    +deleteReview(id, userId)
    +getReviewsByPlace(placeId)
    +getReviewsByUser(userId)
}
note for ReviewService "FR: Service Avis.\n- rating [1..5], pas d'auto-review\n- au plus 1 avis par (user, place)\n- controle auteur pour update/delete\nEN: Review Service.\n- rating [1..5], no self-review\n- at most 1 per (user, place)\n- author check on update/delete"

class AmenityService {
    +createAmenity(amenityData)
    +getAmenityById(id)
    +updateAmenity(id, data)
    +deleteAmenity(id)
    +getAllAmenities()
}
note for AmenityService "FR: Service Equipement.\n- valide nom (unicite, normalisation)\n- CRUD standard\nEN: Amenity Service.\n- validate name (unique/normalized)\n- standard CRUD"

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