// ============================================================================
// HBNB PART 4 - PROFESSIONAL JAVASCRIPT
// Modern, Modular, Accessible Frontend Architecture
// ============================================================================

// ============================================================================
// 1. CONFIGURATION
// ============================================================================

const API_BASE_URL = 'http://localhost:5000/api/v1';

// ============================================================================
// 2. UTILITY FUNCTIONS - Cookie Management
// ============================================================================

/**
 * Set a cookie with name, value and expiration days
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Expiration in days (default 7)
 */
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null
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
 * Delete a cookie by name
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

/**
 * Get authentication token from cookie
 * @returns {string|null} JWT token or null
 */
function getAuthToken() {
    return getCookie('token');
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if authenticated
 */
function isAuthenticated() {
    return getAuthToken() !== null;
}

// ============================================================================
// 3. UI FEEDBACK FUNCTIONS
// ============================================================================

/**
 * Show toast notification (non-intrusive)
 * @param {string} message - Message to display
 * @param {string} type - Type: 'success', 'error', 'info', 'warning'
 * @param {number} duration - Duration in milliseconds (default 4000)
 */
function showToast(message, type = 'info', duration = 4000) {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    
    // Add to body
    document.body.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Show message in specific element
 * @param {string} elementId - ID of element to show message in
 * @param {string} message - Message text
 * @param {string} type - Type: 'success' or 'error'
 */
function showMessage(elementId, message, type = 'error') {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.textContent = message;
    element.className = type === 'success' ? 'success-message' : 'error-message';
    element.style.display = 'block';
    element.setAttribute('role', type === 'success' ? 'status' : 'alert');
    
    // Smooth scroll to message
    element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Hide message element
 * @param {string} elementId - ID of element to hide
 */
function hideMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

/**
 * Show loading state
 * @param {string} elementId - ID of loading element
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
    }
}

/**
 * Hide loading state
 * @param {string} elementId - ID of loading element
 */
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

/**
 * Set button loading state
 * @param {HTMLButtonElement} button - Button element
 * @param {boolean} loading - Loading state
 */
function setButtonLoading(button, loading) {
    if (!button) return;
    
    const buttonText = button.querySelector('.button-text');
    const buttonLoader = button.querySelector('.button-loader');
    
    button.disabled = loading;
    
    if (loading) {
        if (buttonText) buttonText.style.display = 'none';
        if (buttonLoader) buttonLoader.classList.remove('hidden');
    } else {
        if (buttonText) buttonText.style.display = 'inline';
        if (buttonLoader) buttonLoader.classList.add('hidden');
    }
}

// ============================================================================
// 4. API REQUEST HANDLER
// ============================================================================

/**
 * Make API request with error handling and authentication
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} Response data
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getAuthToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    // Add authentication token if not skipped
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        // Handle 401 Unauthorized
        if (response.status === 401) {
            deleteCookie('token');
            const currentPath = window.location.pathname;
            if (!currentPath.includes('login.html')) {
                showToast('Session expired. Please login again.', 'error');
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 1500);
            }
            throw new Error('Unauthorized');
        }
        
        // Handle other HTTP errors
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request failed:', error);
        
        // Show user-friendly error messages
        if (error.message === 'Failed to fetch') {
            throw new Error('Network error. Please check your connection.');
        }
        
        throw error;
    }
}

// ============================================================================
// 5. UTILITY FUNCTIONS - Text Processing
// ============================================================================

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

/**
 * Truncate text to maximum length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, maxLength) {
    if (!text) return '';
    const str = String(text);
    if (str.length <= maxLength) return str;
    return str.slice(0, maxLength) + '...';
}

/**
 * Format date to readable string
 * @param {string} dateString - Date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'Date not available';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (error) {
        return dateString;
    }
}

/**
 * Format price with currency
 * @param {number} price - Price value
 * @returns {string} Formatted price
 */
function formatPrice(price) {
    if (price === null || price === undefined) return '$0';
    return `$${Number(price).toLocaleString()}`;
}

// ============================================================================
// 6. LOGIN PAGE FUNCTIONALITY
// ============================================================================

function initLoginPage() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    
    // Redirect if already authenticated
    if (isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }
    
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const submitButton = loginForm.querySelector('button[type="submit"]');
    
    // Real-time email validation
    if (emailInput) {
        emailInput.addEventListener('blur', () => {
            const emailHint = document.getElementById('email-hint');
            if (emailInput.value && !isValidEmail(emailInput.value)) {
                emailInput.classList.add('error');
                if (emailHint) {
                    emailHint.classList.remove('hidden');
                    emailHint.classList.add('error');
                }
            } else {
                emailInput.classList.remove('error');
                if (emailHint) {
                    emailHint.classList.add('hidden');
                    emailHint.classList.remove('error');
                }
            }
        });
    }
    
    // Form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        hideMessage('error-message');
        hideMessage('success-message');
        
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        
        // Client-side validation
        if (!email || !password) {
            showMessage('error-message', 'Please fill in all fields');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('error-message', 'Please enter a valid email address');
            emailInput.focus();
            return;
        }
        
        setButtonLoading(submitButton, true);
        
        try {
            const data = await apiRequest('/auth/login', {
                method: 'POST',
                skipAuth: true,
                body: JSON.stringify({ email, password })
            });
            
            if (data.access_token) {
                setCookie('token', data.access_token, 7);
                showMessage('success-message', 'Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            } else {
                throw new Error('No token received');
            }
        } catch (error) {
            console.error('Login error:', error);
            showMessage('error-message', error.message || 'Login failed. Please check your credentials.');
            setButtonLoading(submitButton, false);
        }
    });
}

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ============================================================================
// 7. LOGOUT FUNCTIONALITY
// ============================================================================

function logout() {
    deleteCookie('token');
    showToast('Logged out successfully', 'success');
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 1000);
}

// ============================================================================
// 8. INDEX PAGE - PLACES LIST
// ============================================================================

let allPlaces = [];

/**
 * Fetch all places from API
 */
async function fetchPlaces() {
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    const placesListElement = document.getElementById('places-list');
    const emptyState = document.getElementById('empty-state');
    
    if (!placesListElement) return;
    
    showLoading('loading');
    hideMessage('error');
    if (emptyState) emptyState.style.display = 'none';
    
    // Show skeleton loaders
    placesListElement.innerHTML = createSkeletonPlaceCards(6);
    
    try {
        const places = await apiRequest('/places', {
            method: 'GET',
            skipAuth: true
        });
        
        allPlaces = places;
        displayPlaces(places);
        updatePlacesCount(places.length);
    } catch (error) {
        console.error('Error fetching places:', error);
        showMessage('error', 'Failed to load places. Please try again later.');
        placesListElement.innerHTML = '';
    } finally {
        hideLoading('loading');
    }
}

/**
 * Display places in grid
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesListElement = document.getElementById('places-list');
    const emptyState = document.getElementById('empty-state');
    
    if (!placesListElement) return;
    
    if (places.length === 0) {
        placesListElement.innerHTML = '';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }
    
    if (emptyState) emptyState.style.display = 'none';
    
    placesListElement.innerHTML = places.map((place, index) => 
        createPlaceCard(place, index)
    ).join('');
    
    // Add click handlers
    places.forEach((place, index) => {
        const card = placesListElement.children[index];
        if (card) {
            card.addEventListener('click', () => {
                window.location.href = `place.html?id=${place.id}`;
            });
            card.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    window.location.href = `place.html?id=${place.id}`;
                }
            });
        }
    });
}

/**
 * Create HTML for a place card
 * @param {Object} place - Place object
 * @param {number} index - Card index for animation delay
 * @returns {string} HTML string
 */
function createPlaceCard(place, index = 0) {
    const title = escapeHtml(place.title || place.name || 'Unnamed Place');
    const price = formatPrice(place.price || place.price_per_night);
    const description = escapeHtml(truncateText(place.description || 'No description available', 120));
    const animationDelay = `style="animation-delay: ${index * 0.1}s"`;
    
    return `
        <div class="place-card" role="article" tabindex="0" ${animationDelay} 
             aria-label="${title} - ${price} per night">
            <div class="place-card-image"></div>
            <div class="place-card-content">
                <h3 class="place-card-title">${title}</h3>
                <p class="place-card-price">${price} <span style="font-size: var(--fs-sm); font-weight: var(--fw-normal); color: var(--text-light);">/ night</span></p>
                <p class="place-card-description">${description}</p>
                <div class="place-card-footer">
                    <span class="view-details" aria-label="View details for ${title}">View Details →</span>
                </div>
            </div>
        </div>
    `;
}

/**
 * Create skeleton placeholder cards
 * @param {number} count - Number of skeleton cards
 * @returns {string} HTML string
 */
function createSkeletonPlaceCards(count = 6) {
    let html = '';
    for (let i = 0; i < count; i++) {
        html += `
            <div class="skeleton-place-card" aria-hidden="true">
                <div class="skeleton-image"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line short"></div>
                <div class="skeleton-line medium"></div>
            </div>
        `;
    }
    return html;
}

/**
 * Update places count display
 * @param {number} count - Number of places
 */
function updatePlacesCount(count) {
    const countElement = document.getElementById('places-count');
    if (countElement) {
        const text = count === 1 ? '1 place available' : `${count} places available`;
        countElement.textContent = text;
    }
}

/**
 * Filter places by price
 */
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    const maxPrice = parseInt(priceFilter.value);
    
    if (isNaN(maxPrice) || maxPrice === 0) {
        displayPlaces(allPlaces);
        updatePlacesCount(allPlaces.length);
        return;
    }
    
    const filteredPlaces = allPlaces.filter(place => {
        const price = place.price || place.price_per_night || 0;
        return price <= maxPrice;
    });
    
    displayPlaces(filteredPlaces);
    updatePlacesCount(filteredPlaces.length);
    
    // Show toast notification
    showToast(`Showing places up to ${formatPrice(maxPrice)} per night`, 'info', 2000);
}

/**
 * Initialize index page
 */
function initIndexPage() {
    const placesListElement = document.getElementById('places-list');
    if (!placesListElement) return;
    
    fetchPlaces();
    
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
    }
}

// ============================================================================
// 9. PLACE DETAILS PAGE
// ============================================================================

/**
 * Fetch place details by ID
 * @param {string} placeId - Place ID
 */
async function fetchPlaceDetails(placeId) {
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    const placeDetailsElement = document.getElementById('place-details');
    
    if (!placeDetailsElement) return;
    
    showLoading('loading');
    hideMessage('error');
    placeDetailsElement.style.display = 'none';
    
    try {
        const place = await apiRequest(`/places/${placeId}`, {
            method: 'GET',
            skipAuth: true
        });
        
        await displayPlaceDetails(place);
        placeDetailsElement.style.display = 'block';
    } catch (error) {
        console.error('Error fetching place details:', error);
        showMessage('error', 'Failed to load place details. Please try again later.');
    } finally {
        hideLoading('loading');
    }
}

/**
 * Display place details
 * @param {Object} place - Place object
 */
async function displayPlaceDetails(place) {
    if (!place || !place.id) {
        showMessage('error', 'Invalid place data received.');
        return;
    }
    
    // Set title and basic info
    document.getElementById('place-title').textContent = place.title || place.name || 'Unnamed Place';
    document.getElementById('place-price').textContent = `${formatPrice(place.price || place.price_per_night)} / night`;
    document.getElementById('place-description').textContent = place.description || 'No description available.';
    
    // Fetch and display host information
    displayHostInfo(place.owner_id);
    
    // Display amenities
    displayAmenities(place.amenities || []);
    
    // Display location
    document.getElementById('place-latitude').textContent = place.latitude || 'N/A';
    document.getElementById('place-longitude').textContent = place.longitude || 'N/A';
    
    // Display reviews
    displayReviews(place.reviews || []);
    
    // Setup review form
    setupReviewForm(place.id);
}

/**
 * Display host information
 * @param {string} ownerId - Owner/Host ID
 */
async function displayHostInfo(ownerId) {
    const hostElement = document.getElementById('place-host');
    
    if (!ownerId) {
        hostElement.textContent = 'Host information not available';
        return;
    }
    
    hostElement.textContent = 'Loading host information...';
    
    try {
        const host = await apiRequest(`/users/${ownerId}`, {
            method: 'GET',
            skipAuth: true
        });
        
        const hostName = `${host.first_name || ''} ${host.last_name || ''}`.trim() || host.email || 'Unknown Host';
        hostElement.innerHTML = `
            <div style="display: flex; align-items: center; gap: var(--space-3);">
                <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--fw-bold); font-size: var(--fs-lg);">
                    ${hostName.charAt(0).toUpperCase()}
                </div>
                <div>
                    <p style="font-weight: var(--fw-semibold); margin: 0;">${escapeHtml(hostName)}</p>
                    <p style="font-size: var(--fs-sm); color: var(--text-light); margin: 0;">Host</p>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Failed to fetch host info:', error);
        hostElement.textContent = 'Host information not available';
    }
}

/**
 * Display amenities list
 * @param {Array} amenities - Array of amenities
 */
function displayAmenities(amenities) {
    const amenitiesList = document.getElementById('place-amenities');
    
    if (!amenitiesList) return;
    
    if (!amenities || amenities.length === 0) {
        amenitiesList.innerHTML = '<li>No amenities listed</li>';
        return;
    }
    
    amenitiesList.innerHTML = amenities.map(amenity => {
        const amenityName = typeof amenity === 'object' ? amenity.name : amenity;
        return `<li>${escapeHtml(amenityName)}</li>`;
    }).join('');
}

/**
 * Display reviews list
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    
    if (!reviewsList) return;
    
    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = `
            <div class="no-reviews" role="status">
                <p style="font-size: var(--fs-lg); color: var(--text-secondary);">No reviews yet. Be the first to review!</p>
            </div>
        `;
        return;
    }
    
    reviewsList.innerHTML = reviews.map(review => createReviewCard(review)).join('');
    
    // Update review statistics
    updateReviewStats(reviews);
}

/**
 * Create HTML for a review card
 * @param {Object} review - Review object
 * @returns {string} HTML string
 */
function createReviewCard(review) {
    const userName = escapeHtml(review.user_name || 'Anonymous');
    const rating = review.rating || 0;
    const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
    const text = escapeHtml(review.text || review.comment || '');
    const date = formatDate(review.created_at || review.date);
    
    return `
        <div class="review-card" role="article">
            <div class="review-header">
                <div style="display: flex; align-items: center; gap: var(--space-3);">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: var(--fw-bold);">
                        ${userName.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h4 style="margin: 0; font-size: var(--fs-base);">${userName}</h4>
                        <span class="review-rating" aria-label="${rating} stars">${stars}</span>
                    </div>
                </div>
            </div>
            <p class="review-text">${text}</p>
            <p class="review-date">${date}</p>
        </div>
    `;
}

/**
 * Update review statistics
 * @param {Array} reviews - Array of reviews
 */
function updateReviewStats(reviews) {
    const averageRatingElement = document.getElementById('average-rating');
    const totalReviewsElement = document.getElementById('total-reviews');
    
    if (!reviews || reviews.length === 0) return;
    
    const totalRating = reviews.reduce((sum, review) => sum + (review.rating || 0), 0);
    const averageRating = (totalRating / reviews.length).toFixed(1);
    
    if (averageRatingElement) {
        averageRatingElement.textContent = `${averageRating} ★`;
    }
    
    if (totalReviewsElement) {
        totalReviewsElement.textContent = `(${reviews.length} ${reviews.length === 1 ? 'review' : 'reviews'})`;
    }
}

/**
 * Setup review form with validation and submission
 * @param {string} placeId - Place ID
 */
function setupReviewForm(placeId) {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;
    
    // Show/hide form based on authentication
    if (!isAuthenticated()) {
        reviewForm.innerHTML = `
            <div class="login-required-message">
                <p>You must be <a href="login.html">logged in</a> to leave a review.</p>
            </div>
        `;
        return;
    }
    
    const reviewText = document.getElementById('review-text');
    const submitButton = reviewForm.querySelector('button[type="submit"]');
    const ratingInputs = reviewForm.querySelectorAll('input[name="rating"]');
    const ratingText = document.getElementById('rating-text');
    
    // Character count for review text
    if (reviewText) {
        const charCount = document.getElementById('char-count');
        reviewText.addEventListener('input', () => {
            if (charCount) {
                charCount.textContent = reviewText.value.length;
            }
        });
    }
    
    // Rating selection feedback
    ratingInputs.forEach(input => {
        input.addEventListener('change', () => {
            const ratingValue = input.value;
            const ratingLabels = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
            if (ratingText) {
                ratingText.textContent = `${ratingLabels[ratingValue]} (${ratingValue} star${ratingValue > 1 ? 's' : ''})`;
            }
        });
    });
    
    // Form submission
    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        hideMessage('review-error');
        hideMessage('review-success');
        
        const rating = reviewForm.querySelector('input[name="rating"]:checked')?.value;
        const text = reviewText?.value.trim();
        
        // Validation
        if (!rating) {
            showMessage('review-error', 'Please select a rating');
            return;
        }
        
        if (!text || text.length < 10) {
            showMessage('review-error', 'Review must be at least 10 characters long');
            reviewText?.focus();
            return;
        }
        
        setButtonLoading(submitButton, true);
        
        try {
            await apiRequest(`/places/${placeId}/reviews`, {
                method: 'POST',
                body: JSON.stringify({
                    text: text,
                    rating: parseInt(rating, 10)
                })
            });
            
            showMessage('review-success', 'Review submitted successfully!');
            showToast('Thank you for your review!', 'success');
            
            // Reset form
            reviewForm.reset();
            if (ratingText) ratingText.textContent = 'Select your rating';
            if (charCount) charCount.textContent = '0';
            
            // Reload reviews after 1.5 seconds
            setTimeout(() => {
                fetchPlaceDetails(placeId);
            }, 1500);
        } catch (error) {
            console.error('Review submission error:', error);
            showMessage('review-error', error.message || 'Failed to submit review. Please try again.');
        } finally {
            setButtonLoading(submitButton, false);
        }
    });
}

/**
 * Initialize place details page
 */
function initPlaceDetailsPage() {
    const placeDetailsElement = document.getElementById('place-details');
    if (!placeDetailsElement) return;
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        showMessage('error', 'No place ID provided.');
        return;
    }
    
    fetchPlaceDetails(placeId);
}

// ============================================================================
// 10. ADD REVIEW PAGE (STANDALONE)
// ============================================================================

function initAddReviewPage() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;
    
    // Check authentication
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');
    
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }
    
    // Setup similar to inline review form
    const reviewText = document.getElementById('review-text');
    const submitButton = reviewForm.querySelector('button[type="submit"]');
    const cancelButton = document.getElementById('cancel-button');
    const ratingInputs = reviewForm.querySelectorAll('input[name="rating"]');
    const ratingText = document.getElementById('rating-text');
    const charCount = document.getElementById('char-count');
    
    // Character count
    if (reviewText && charCount) {
        reviewText.addEventListener('input', () => {
            charCount.textContent = reviewText.value.length;
        });
    }
    
    // Rating feedback
    ratingInputs.forEach(input => {
        input.addEventListener('change', () => {
            const ratingValue = input.value;
            const ratingLabels = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
            if (ratingText) {
                ratingText.textContent = `${ratingLabels[ratingValue]} (${ratingValue} star${ratingValue > 1 ? 's' : ''})`;
            }
        });
    });
    
    // Cancel button
    if (cancelButton) {
        cancelButton.addEventListener('click', () => {
            window.location.href = `place.html?id=${placeId}`;
        });
    }
    
    // Form submission
    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        hideMessage('error-message');
        hideMessage('success-message');
        
        const rating = reviewForm.querySelector('input[name="rating"]:checked')?.value;
        const text = reviewText?.value.trim();
        
        // Validation
        if (!rating) {
            showMessage('error-message', 'Please select a rating');
            return;
        }
        
        if (!text || text.length < 10) {
            showMessage('error-message', 'Review must be at least 10 characters long');
            reviewText?.focus();
            return;
        }
        
        setButtonLoading(submitButton, true);
        
        try {
            await apiRequest(`/places/${placeId}/reviews`, {
                method: 'POST',
                body: JSON.stringify({
                    text: text,
                    rating: parseInt(rating, 10)
                })
            });
            
            showMessage('success-message', 'Review submitted successfully! Redirecting...');
            
            // Redirect after success
            setTimeout(() => {
                window.location.href = `place.html?id=${placeId}`;
            }, 1500);
        } catch (error) {
            console.error('Review submission error:', error);
            showMessage('error-message', error.message || 'Failed to submit review. Please try again.');
            setButtonLoading(submitButton, false);
        }
    });
}

// ============================================================================
// 11. NAVIGATION & AUTHENTICATION STATE
// ============================================================================

/**
 * Update navigation based on authentication state
 */
function updateNavigationAuth() {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;
    
    if (isAuthenticated()) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.onclick = (e) => {
            e.preventDefault();
            logout();
        };
    } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        loginLink.onclick = null;
    }
}

// ============================================================================
// 12. PAGE INITIALIZATION
// ============================================================================

/**
 * Initialize appropriate page based on URL
 */
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const filename = path.split('/').pop() || 'index.html';
    
    // Update navigation auth state on all pages
    updateNavigationAuth();
    
    // Initialize appropriate page
    if (path.includes('login.html')) {
        initLoginPage();
    } else if (path.includes('place.html')) {
        initPlaceDetailsPage();
    } else if (path.includes('add_review.html')) {
        initAddReviewPage();
    } else if (path.includes('index.html') || path.endsWith('/') || filename === '') {
        initIndexPage();
    }
});

// ============================================================================
// 13. GLOBAL ERROR HANDLING
// ============================================================================

// Handle uncaught errors gracefully
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showToast('An unexpected error occurred. Please refresh the page.', 'error');
});

// Handle promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
