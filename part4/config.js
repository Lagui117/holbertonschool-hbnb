// Configuration de l'Application HBnB Part 4
// Ce fichier permet de personnaliser facilement l'application

const CONFIG = {
    // URL de l'API Backend (Part 3)
    API_BASE_URL: 'http://localhost:5000/api/v1',
    
    // Durée de validité du cookie JWT (en jours)
    COOKIE_EXPIRY_DAYS: 7,
    
    // Nom du cookie contenant le token JWT
    COOKIE_NAME: 'token',
    
    // Configuration du filtre de prix - CONFORME AUX SPECS (10, 50, 100, All)
    PRICE_FILTERS: [
        { value: 'all', label: 'All' },
        { value: '10', label: '$10', max: 10 },
        { value: '50', label: '$50', max: 50 },
        { value: '100', label: '$100', max: 100 }
    ],
    
    // Longueur minimale des reviews
    REVIEW_MIN_LENGTH: 10,
    
    // Nombre de caractères max pour le résumé des descriptions
    DESCRIPTION_TRUNCATE_LENGTH: 100,
    
    // Messages d'erreur personnalisables
    MESSAGES: {
        LOGIN_FAILED: 'Login failed. Please check your credentials.',
        LOAD_PLACES_FAILED: 'Failed to load places. Please try again later.',
        LOAD_PLACE_FAILED: 'Failed to load place details. Please try again later.',
        SUBMIT_REVIEW_FAILED: 'Failed to submit review. Please try again.',
        REVIEW_SUCCESS: 'Review submitted successfully!',
        UNAUTHORIZED: 'You must be logged in to perform this action.',
        NO_PLACES_FOUND: 'No places found matching your criteria.',
        NO_REVIEWS: 'No reviews yet. Be the first to review!',
        LOADING: 'Loading...',
        SELECT_RATING: 'Please select a rating.',
        INVALID_PLACE_ID: 'No place ID provided.'
    },
    
    // Configuration du formatage des dates
    DATE_FORMAT: {
        locale: 'en-US',
        options: {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }
    },
    
    // Temps de redirection après succès (en millisecondes)
    REDIRECT_DELAY: 2000,
    
    // Activer/désactiver les logs de debug dans la console
    DEBUG_MODE: true
};

// Export de la configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
