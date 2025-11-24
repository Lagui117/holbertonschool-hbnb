/**
 * HBnB Part 4 - Professional Web Client
 * Modern, Accessible, Optimized JavaScript ES6
 * 
 * NO FRAMEWORKS - Pure Vanilla JS
 * Uses Fetch API for all HTTP requests
 * JWT stored in cookies only (not localStorage)
 * 
 * FEATURES:
 * - Enhanced UX with loading states
 * - Better error handling & user feedback
 * - Accessibility improvements
 * - Input validation & sanitization
 * - Responsive & performant
 */

'use strict';

// ============================================================================
// CONFIGURATION & CONSTANTS
// ============================================================================

const API_BASE_URL = CONFIG?.API_BASE_URL || 'http://localhost:5000/api/v1';
const COOKIE_NAME = CONFIG?.COOKIE_NAME || 'token';
const COOKIE_EXPIRY_DAYS = CONFIG?.COOKIE_EXPIRY_DAYS || 7;

// ============================================================================
// UI UTILITY FUNCTIONS - Enhanced User Experience
// ============================================================================

/**
 * Show/hide loading state on button
 * @param {HTMLButtonElement} button - Button element
 * @param {boolean} isLoading - Loading state
 */
function toggleButtonLoading(button, isLoading) {
    if (!button) return;
    
    const textEl = button.querySelector('.button-text');
    const loaderEl = button.querySelector('.button-loader');
    
    button.disabled = isLoading;
    
    if (textEl && loaderEl) {
        if (isLoading) {
            textEl.style.display = 'none';
            loaderEl.classList.remove('hidden');
        } else {
            textEl.style.display = 'inline';
            loaderEl.classList.add('hidden');
        }
    }
}

/**
 * Show message to user
 * @param {string} elementId - ID of message container
 * @param {string} message - Message text
 * @param {string} type - Message type: 'success', 'error', 'info'
 */
function showMessage(elementId, message, type = 'error') {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.textContent = message;
    element.className = `${type}-message`;
    element.style.display = 'block';
    element.setAttribute('role', type === 'error' ? 'alert' : 'status');
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
}

/**
 * Hide message
 * @param {string} elementId - ID of message container
 */
function hideMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

/**
 * Show toast notification (non-blocking)
 * @param {string} message - Message text
 * @param {string} type - Type: 'success', 'error', 'info'
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Validate email format
 * @param {string} email - Email address
 * @returns {boolean} Valid email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Debounce function for performance
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Show/hide loading state
 * @param {boolean} show - Show or hide
 */
function toggleLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'block' : 'none';
    }
}

/**
 * Show/hide error
 * @param {string} message - Error message (empty to hide)
 */
function toggleError(message = '') {
    const error = document.getElementById('error');
    if (error) {
        if (message) {
            error.textContent = message;
            error.style.display = 'block';
        } else {
            error.style.display = 'none';
        }
    }
}

// ============================================================================
// COOKIE MANAGEMENT FUNCTIONS
// ============================================================================

/**
 * Set a cookie with name, value and expiry days
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Days until expiration
 */
function setCookie(name, value, days = COOKIE_EXPIRY_DAYS) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

/**
 * Delete a cookie
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

/**
 * Get auth token from cookie
 * @returns {string|null} JWT token or null
 */
function getAuthToken() {
    return getCookie(COOKIE_NAME);
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if authenticated
 */
function checkAuthentication() {
    return getAuthToken() !== null;
}

// ============================================================================
// API REQUEST FUNCTIONS
// ============================================================================

/**
 * Make an API request with automatic token handling
 * @param {string} endpoint - API endpoint (e.g., '/places')
 * @param {object} options - Fetch options
 * @returns {Promise<object>} Response data
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getAuthToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    // Add auth token if available and not explicitly skipped
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        // Handle 401 Unauthorized - redirect to login
        if (response.status === 401) {
            deleteCookie(COOKIE_NAME);
            const currentPath = window.location.pathname;
            if (!currentPath.includes('login.html')) {
                window.location.href = 'login.html';
            }
            throw new Error('Unauthorized');
        }
        
        // Handle other errors
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

// ============================================================================
// LOGIN PAGE FUNCTIONS (Task 2)
// ============================================================================

/**
 * Initialize login page functionality
 */
function initLoginPage() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    
    // If already authenticated, redirect to index
    if (checkAuthentication()) {
        window.location.href = 'index.html';
        return;
    }
    
    loginForm.addEventListener('submit', loginUser);
}

/**
 * Handle login form submission with improved UX
 * @param {Event} e - Submit event
 */
async function loginUser(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const submitButton = e.target.querySelector('button[type="submit"]');
    
    // Hide previous messages
    hideMessage('error-message');
    hideMessage('success-message');
    
    // Validate inputs
    if (!email || !password) {
        showMessage('error-message', 'Please enter both email and password.', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showMessage('error-message', 'Please enter a valid email address.', 'error');
        document.getElementById('email').focus();
        return;
    }
    
    // Show loading state
    toggleButtonLoading(submitButton, true);
    
    try {
        // POST to /auth/login endpoint
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            skipAuth: true,
            body: JSON.stringify({ email, password })
        });
        
        // Store JWT token in cookie
        if (data.access_token) {
            setCookie(COOKIE_NAME, data.access_token);
            showMessage('success-message', 'Login successful! Redirecting...', 'success');
            
            // Redirect after short delay for UX
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 500);
        } else {
            throw new Error('No authentication token received from server.');
        }
    } catch (error) {
        console.error('Login error:', error);
        let errorMessage = 'Login failed. Please check your credentials and try again.';
        
        if (error.message.includes('401') || error.message.includes('Unauthorized')) {
            errorMessage = 'Invalid email or password. Please try again.';
        } else if (error.message.includes('network') || error.message.includes('Failed to fetch')) {
            errorMessage = 'Network error. Please check your connection and try again.';
        }
        
        showMessage('error-message', errorMessage, 'error');
    } finally {
        toggleButtonLoading(submitButton, false);
    }
}

// ============================================================================
// LOGOUT FUNCTION
// ============================================================================

/**
 * Logout user - delete cookie and redirect to login
 */
function logout() {
    deleteCookie(COOKIE_NAME);
    window.location.href = 'login.html';
}

// ============================================================================
// INDEX PAGE FUNCTIONS (Task 3) - Places List
// ============================================================================

let allPlaces = []; // Store all places for filtering

/**
 * Initialize index page - fetch and display places
 */
function initIndexPage() {
    updateLoginButton();
    
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
        fetchPlaces();
    }
}

/**
 * Update login/logout button based on authentication status
 */
function updateLoginButton() {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;
    
    if (checkAuthentication()) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.classList.add('login-button');
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        loginLink.classList.add('login-button');
    }
}

/**
 * Fetch all places from API
 */
async function fetchPlaces() {
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    const placesListElement = document.getElementById('places-list');
    
    if (!placesListElement) return;
    
    loadingElement.style.display = 'block';
    errorElement.style.display = 'none';
    
    try {
        // GET /places - no auth required
        const places = await apiRequest('/places', {
            method: 'GET',
            skipAuth: true
        });
        
        allPlaces = places;
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
        errorElement.textContent = 'Failed to load places. Please try again later.';
        errorElement.style.display = 'block';
    } finally {
        loadingElement.style.display = 'none';
    }
}

/**
 * Display places in grid with place-card class
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesListElement = document.getElementById('places-list');
    if (!placesListElement) return;
    
    if (places.length === 0) {
        placesListElement.innerHTML = '<p class="no-results">No places found matching your criteria.</p>';
        return;
    }
    
    // Generate place cards - MUST have class="place-card"
    placesListElement.innerHTML = places.map(place => `
        <div class="place-card" onclick="window.location.href='place.html?id=${place.id}'">
            <div class="place-card-content">
                <h3>${escapeHtml(place.title || place.name || 'Unnamed Place')}</h3>
                <p class="place-card-price">$${place.price || 0} / night</p>
                <p class="place-description">${escapeHtml(truncateText(place.description || 'No description available', 100))}</p>
                <div class="place-card-footer">
                    <a href="place.html?id=${place.id}" class="details-button" onclick="event.stopPropagation()">View Details</a>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Filter places by price - SPEC: 10, 50, 100, All
 */
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    const selectedValue = priceFilter.value;
    
    if (selectedValue === 'all') {
        displayPlaces(allPlaces);
        return;
    }
    
    // Filter by maximum price (10, 50, or 100)
    const maxPrice = parseInt(selectedValue);
    const filteredPlaces = allPlaces.filter(place => {
        const price = place.price || 0;
        return price <= maxPrice;
    });
    
    displayPlaces(filteredPlaces);
}

// ============================================================================
// PLACE DETAILS PAGE FUNCTIONS (Task 4)
// ============================================================================

/**
 * Initialize place details page
 */
function initPlaceDetailsPage() {
    updateLoginButton();
    fetchPlaceDetails();
}

/**
 * Fetch and display place details including reviews
 */
async function fetchPlaceDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        document.getElementById('error').textContent = 'No place ID provided.';
        document.getElementById('error').style.display = 'block';
        return;
    }
    
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    
    loadingElement.style.display = 'block';
    errorElement.style.display = 'none';
    
    try {
        // GET /places/:id
        const place = await apiRequest(`/places/${placeId}`, {
            method: 'GET',
            skipAuth: true
        });
        
        displayPlaceDetails(place);
        await fetchReviews(placeId);
        setupReviewForm(placeId);
    } catch (error) {
        console.error('Error fetching place details:', error);
        errorElement.textContent = 'Failed to load place details. Please try again later.';
        errorElement.style.display = 'block';
    } finally {
        loadingElement.style.display = 'none';
    }
}

/**
 * Display place details - name, description, price, host, amenities
 * @param {object} place - Place object
 */
function displayPlaceDetails(place) {
    // Show the place details section
    const placeDetailsElement = document.getElementById('place-details');
    if (placeDetailsElement) {
        placeDetailsElement.style.display = 'block';
    }
    
    // Display basic information
    document.getElementById('place-title').textContent = place.title || place.name || 'Unnamed Place';
    document.getElementById('place-price').textContent = `$${place.price || 0} per night`;
    document.getElementById('place-description').textContent = place.description || 'No description available';
    
    // Display host information
    const hostName = `${place.owner_first_name || 'Unknown'} ${place.owner_last_name || ''}`;
    document.getElementById('place-host').textContent = `Hosted by ${hostName}`;
    
    // Display location
    const latitudeElement = document.getElementById('place-latitude');
    const longitudeElement = document.getElementById('place-longitude');
    if (latitudeElement && longitudeElement) {
        latitudeElement.textContent = place.latitude || 'N/A';
        longitudeElement.textContent = place.longitude || 'N/A';
    }
    
    // Display amenities
    const amenitiesContainer = document.getElementById('place-amenities');
    if (place.amenities && place.amenities.length > 0) {
        amenitiesContainer.innerHTML = place.amenities.map(amenity => 
            `<li class="amenity-item">${escapeHtml(amenity.name || amenity)}</li>`
        ).join('');
    } else {
        amenitiesContainer.innerHTML = '<li>No amenities listed</li>';
    }
}

/**
 * Fetch and display reviews for a place
 * @param {string} placeId - Place ID
 */
async function fetchReviews(placeId) {
    try {
        // GET /places/:id/reviews
        const reviews = await apiRequest(`/places/${placeId}/reviews`, {
            method: 'GET',
            skipAuth: true
        });
        
        displayReviews(reviews);
    } catch (error) {
        console.error('Error fetching reviews:', error);
        document.getElementById('reviews-list').innerHTML = '<p>Failed to load reviews.</p>';
    }
}

/**
 * Display reviews with review-card class (SPEC requirement)
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    
    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review!</p>';
        updateReviewsStats(0, 0);
        return;
    }
    
    // Calculate average rating
    const avgRating = reviews.reduce((sum, r) => sum + (r.rating || 0), 0) / reviews.length;
    updateReviewsStats(avgRating, reviews.length);
    
    // MUST use class="review-card" per specs
    reviewsList.innerHTML = reviews.map(review => `
        <div class="review-card">
            <div class="review-header">
                <h4>${escapeHtml(review.user_first_name || 'Anonymous')} ${escapeHtml(review.user_last_name || '')}</h4>
                <div class="review-rating">${'★'.repeat(review.rating || 0)}${'☆'.repeat(5 - (review.rating || 0))}</div>
            </div>
            <p class="review-text">${escapeHtml(review.text || review.comment || '')}</p>
            <p class="review-date">${formatDate(review.created_at)}</p>
        </div>
    `).join('');
}

/**
 * Update reviews statistics display
 * @param {number} avgRating - Average rating
 * @param {number} totalReviews - Total number of reviews
 */
function updateReviewsStats(avgRating, totalReviews) {
    const avgElement = document.getElementById('average-rating');
    const totalElement = document.getElementById('total-reviews');
    
    if (avgElement && totalElement) {
        if (totalReviews > 0) {
            avgElement.textContent = `★ ${avgRating.toFixed(1)}`;
            totalElement.textContent = `(${totalReviews} review${totalReviews !== 1 ? 's' : ''})`;
        } else {
            avgElement.textContent = '';
            totalElement.textContent = 'No reviews yet';
        }
    }
}

/**
 * Setup review form - show/hide based on authentication
 * @param {string} placeId - Place ID
 */
function setupReviewForm(placeId) {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;
    
    // Check authentication - if not logged in, hide form
    if (!checkAuthentication()) {
        reviewForm.style.display = 'none';
        const reviewSection = document.getElementById('review-section');
        if (reviewSection) {
            const loginMessage = document.createElement('p');
            loginMessage.className = 'login-required-message';
            loginMessage.innerHTML = 'Please <a href="login.html">login</a> to leave a review.';
            reviewSection.insertBefore(loginMessage, reviewForm);
        }
    } else {
        reviewForm.style.display = 'block';
        
        // Setup star rating interactivity
        setupStarRating();
        
        // Setup character counter
        setupCharacterCounter();
        
        reviewForm.addEventListener('submit', (e) => handleReviewSubmit(e, placeId));
    }
}

/**
 * Setup interactive star rating system
 */
function setupStarRating() {
    const stars = document.querySelectorAll('.star-rating .star');
    const ratingText = document.getElementById('rating-text');
    const ratingLabels = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
    
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const rating = 5 - index;
            if (ratingText) {
                ratingText.textContent = `${rating} - ${ratingLabels[rating - 1]}`;
                ratingText.style.color = '#FFB400';
            }
        });
    });
}

/**
 * Setup character counter for review text
 */
function setupCharacterCounter() {
    const reviewText = document.getElementById('review-text');
    const charCount = document.getElementById('char-count');
    
    if (reviewText && charCount) {
        reviewText.addEventListener('input', () => {
            const count = reviewText.value.length;
            charCount.textContent = count;
            
            if (count < 10) {
                charCount.style.color = '#dc3545';
            } else {
                charCount.style.color = '#28a745';
            }
        });
    }
}

/**
 * Handle review form submission
 * @param {Event} e - Submit event
 * @param {string} placeId - Place ID
 */
async function handleReviewSubmit(e, placeId) {
    e.preventDefault();
    
    const rating = document.querySelector('input[name="rating"]:checked');
    const reviewText = document.getElementById('review-text').value;
    const errorElement = document.getElementById('review-error');
    const successElement = document.getElementById('review-success');
    
    errorElement.style.display = 'none';
    successElement.style.display = 'none';
    
    if (!rating) {
        errorElement.textContent = 'Please select a rating.';
        errorElement.style.display = 'block';
        return;
    }
    
    try {
        // POST /places/:id/reviews - requires authentication
        await apiRequest(`/places/${placeId}/reviews`, {
            method: 'POST',
            body: JSON.stringify({
                rating: parseInt(rating.value),
                text: reviewText
            })
        });
        
        successElement.textContent = 'Review submitted successfully!';
        successElement.style.display = 'block';
        
        // Reset form
        e.target.reset();
        
        // Refresh reviews
        await fetchReviews(placeId);
        
        // Hide success message after 3 seconds
        setTimeout(() => {
            successElement.style.display = 'none';
        }, 3000);
    } catch (error) {
        console.error('Error submitting review:', error);
        errorElement.textContent = error.message || 'Failed to submit review. Please try again.';
        errorElement.style.display = 'block';
    }
}

// ============================================================================
// ADD REVIEW PAGE FUNCTIONS (Task 5)
// ============================================================================

/**
 * Initialize add review page (standalone page)
 */
function initAddReviewPage() {
    // Check authentication first
    if (!checkAuthentication()) {
        window.location.href = 'index.html';
        return;
    }
    
    updateLoginButton();
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        document.getElementById('error-message').textContent = 'No place ID provided.';
        document.getElementById('error-message').style.display = 'block';
        return;
    }
    
    // Setup cancel button
    const cancelButton = document.getElementById('cancel-button');
    if (cancelButton) {
        cancelButton.addEventListener('click', () => {
            window.location.href = `place.html?id=${placeId}`;
        });
    }
    
    // Setup form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => submitReview(e, placeId));
    }
}

/**
 * Submit review from add_review.html page
 * @param {Event} e - Submit event
 * @param {string} placeId - Place ID
 */
async function submitReview(e, placeId) {
    e.preventDefault();
    
    const rating = document.getElementById('review-rating').value;
    const reviewText = document.getElementById('review-text').value;
    const errorElement = document.getElementById('error-message');
    const successElement = document.getElementById('success-message');
    
    errorElement.style.display = 'none';
    successElement.style.display = 'none';
    
    if (!rating) {
        errorElement.textContent = 'Please select a rating.';
        errorElement.style.display = 'block';
        return;
    }
    
    if (reviewText.length < 10) {
        errorElement.textContent = 'Review must be at least 10 characters long.';
        errorElement.style.display = 'block';
        return;
    }
    
    try {
        // POST /places/:id/reviews
        await apiRequest(`/places/${placeId}/reviews`, {
            method: 'POST',
            body: JSON.stringify({
                rating: parseInt(rating),
                text: reviewText
            })
        });
        
        successElement.textContent = 'Review submitted successfully! Redirecting...';
        successElement.style.display = 'block';
        
        // Redirect back to place details after 2 seconds
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 2000);
    } catch (error) {
        console.error('Error submitting review:', error);
        errorElement.textContent = error.message || 'Failed to submit review. Please try again.';
        errorElement.style.display = 'block';
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Format date string to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ============================================================================
// PAGE INITIALIZATION - ROUTER
// ============================================================================

/**
 * Initialize the appropriate page based on current URL
 */
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    
    if (path.includes('login.html')) {
        initLoginPage();
    } else if (path.includes('place.html')) {
        initPlaceDetailsPage();
    } else if (path.includes('add_review.html')) {
        initAddReviewPage();
    } else if (path.includes('index.html') || path === '/' || path.endsWith('/part4/') || path.endsWith('/part4')) {
        initIndexPage();
    }
});
