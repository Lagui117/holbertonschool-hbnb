## High-Level Class Diagram (Task 1)

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
