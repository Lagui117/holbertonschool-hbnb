// ============================================================================
// COOKIE MANAGEMENT
// ============================================================================

function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

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

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

// ============================================================================
// AUTHENTICATION
// ============================================================================

function checkAuthentication() {
    const token = getCookie(CONFIG.COOKIE_NAME);
    const loginLink = document.getElementById('login-link');
    
    if (token && loginLink) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.onclick = (e) => {
            e.preventDefault();
            logout();
        };
    }
    
    return token;
}

function logout() {
    deleteCookie(CONFIG.COOKIE_NAME);
    window.location.href = 'index.html';
}

// ============================================================================
// API CALLS
// ============================================================================

async function apiCall(endpoint, options = {}) {
    const token = getCookie(CONFIG.COOKIE_NAME);
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || data.message || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ============================================================================
// LOGIN PAGE
// ============================================================================

if (document.getElementById('login-form')) {
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('error-message');
        const submitButton = e.target.querySelector('button[type="submit"]');
        
        errorDiv.style.display = 'none';
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';
        
        try {
            const data = await apiCall('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            
            if (data.access_token) {
                setCookie(CONFIG.COOKIE_NAME, data.access_token, CONFIG.COOKIE_EXPIRY_DAYS);
                window.location.href = 'index.html';
            }
        } catch (error) {
            errorDiv.textContent = error.message || 'Invalid email or password';
            errorDiv.style.display = 'block';
            submitButton.disabled = false;
            submitButton.textContent = 'Login';
        }
    });
}

// ============================================================================
// INDEX PAGE - PLACES LIST
// ============================================================================

if (document.getElementById('places')) {
    checkAuthentication();
    
    let allPlaces = [];
    
    async function loadPlaces() {
        const placesContainer = document.getElementById('places');
        const loadingEl = document.getElementById('loading');
        
        try {
            const places = await apiCall('/places/');
            allPlaces = places;
            
            loadingEl.style.display = 'none';
            displayPlaces(places);
        } catch (error) {
            loadingEl.textContent = 'Error loading places: ' + error.message;
        }
    }
    
    function displayPlaces(places) {
        const placesContainer = document.getElementById('places');
        placesContainer.innerHTML = '';
        
        if (places.length === 0) {
            placesContainer.innerHTML = '<p>No places found.</p>';
            return;
        }
        
        places.forEach(place => {
            const placeCard = document.createElement('div');
            placeCard.className = 'place-card';
            
            placeCard.innerHTML = `
                <div class="place-card-content">
                    <h3>${escapeHtml(place.title)}</h3>
                    <p class="price">$${place.price}/night</p>
                    <p>${escapeHtml(place.description || 'No description available')}</p>
                    <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
                </div>
            `;
            
            placesContainer.appendChild(placeCard);
        });
    }
    
    // Price filter
    document.getElementById('price-filter').addEventListener('change', (e) => {
        const maxPrice = e.target.value;
        
        if (!maxPrice) {
            displayPlaces(allPlaces);
            return;
        }
        
        const filtered = allPlaces.filter(place => 
            place.price <= parseInt(maxPrice)
        );
        
        displayPlaces(filtered);
    });
    
    loadPlaces();
}

// ============================================================================
// PLACE DETAILS PAGE
// ============================================================================

if (document.getElementById('place-details')) {
    checkAuthentication();
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        document.getElementById('loading').textContent = 'No place ID provided';
    } else {
        loadPlaceDetails(placeId);
    }
    
    async function loadPlaceDetails(id) {
        const loadingEl = document.getElementById('loading');
        const errorEl = document.getElementById('error-message');
        const detailsEl = document.getElementById('place-details');
        
        try {
            const place = await apiCall(`/places/${id}`);
            
            loadingEl.style.display = 'none';
            detailsEl.style.display = 'block';
            
            // Display place details
            document.getElementById('place-title').textContent = place.title;
            document.getElementById('place-price').textContent = `$${place.price}/night`;
            document.getElementById('place-description').textContent = place.description || 'No description';
            document.getElementById('place-host').textContent = `Host ID: ${place.owner_id}`;
            document.getElementById('place-latitude').textContent = place.latitude;
            document.getElementById('place-longitude').textContent = place.longitude;
            
            // Display amenities
            const amenitiesList = document.getElementById('place-amenities');
            amenitiesList.innerHTML = '';
            
            if (place.amenities && place.amenities.length > 0) {
                for (const amenityId of place.amenities) {
                    try {
                        const amenity = await apiCall(`/amenities/${amenityId}`);
                        const li = document.createElement('li');
                        li.textContent = amenity.name;
                        amenitiesList.appendChild(li);
                    } catch (e) {
                        console.error('Error loading amenity:', e);
                    }
                }
            } else {
                amenitiesList.innerHTML = '<li>No amenities</li>';
            }
            
            // Load reviews
            loadReviews(id);
            
            // Show review form if authenticated
            const token = getCookie(CONFIG.COOKIE_NAME);
            if (token) {
                document.getElementById('add-review').style.display = 'block';
                setupReviewForm(id);
            }
            
        } catch (error) {
            loadingEl.style.display = 'none';
            errorEl.textContent = 'Error loading place: ' + error.message;
            errorEl.style.display = 'block';
        }
    }
    
    async function loadReviews(placeId) {
        const reviewsList = document.getElementById('reviews-list');
        
        try {
            const reviews = await apiCall(`/reviews/places/${placeId}/reviews`);
            
            reviewsList.innerHTML = '';
            
            if (reviews.length === 0) {
                reviewsList.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
                return;
            }
            
            reviews.forEach(review => {
                const reviewDiv = document.createElement('div');
                reviewDiv.className = 'review-card';
                
                const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
                
                reviewDiv.innerHTML = `
                    <div class="review-header">
                        <span class="review-author">User ${review.user_id}</span>
                        <span class="review-rating">${stars}</span>
                    </div>
                    <p class="review-text">${escapeHtml(review.text)}</p>
                `;
                
                reviewsList.appendChild(reviewDiv);
            });
        } catch (error) {
            reviewsList.innerHTML = '<p>Error loading reviews</p>';
        }
    }
    
    function setupReviewForm(placeId) {
        const form = document.getElementById('review-form');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const rating = document.getElementById('rating').value;
            const text = document.getElementById('review-text').value;
            const submitButton = form.querySelector('button[type="submit"]');
            
            if (!rating) {
                alert('Please select a rating');
                return;
            }
            
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
            
            try {
                await apiCall('/reviews/', {
                    method: 'POST',
                    body: JSON.stringify({
                        place_id: placeId,
                        rating: parseInt(rating),
                        text: text
                    })
                });
                
                alert('Review submitted successfully!');
                form.reset();
                loadReviews(placeId);
            } catch (error) {
                alert('Error submitting review: ' + error.message);
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
        });
    }
}

// ============================================================================
// ADD REVIEW PAGE (add_review.html)
// ============================================================================

if (document.getElementById('review-form') && window.location.pathname.includes('add_review')) {
    const token = checkAuthentication();
    
    if (!token) {
        window.location.href = 'index.html';
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');
    
    if (!placeId) {
        document.getElementById('error-message').textContent = 'No place ID provided';
        document.getElementById('error-message').style.display = 'block';
    } else {
        document.getElementById('review-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const rating = document.getElementById('rating').value;
            const text = document.getElementById('review-text').value;
            const errorDiv = document.getElementById('error-message');
            const submitButton = e.target.querySelector('button[type="submit"]');
            
            if (!rating) {
                errorDiv.textContent = 'Please select a rating';
                errorDiv.style.display = 'block';
                return;
            }
            
            errorDiv.style.display = 'none';
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
            
            try {
                await apiCall('/reviews/', {
                    method: 'POST',
                    body: JSON.stringify({
                        place_id: placeId,
                        rating: parseInt(rating),
                        text: text
                    })
                });
                
                alert('Review submitted successfully!');
                window.location.href = `place.html?id=${placeId}`;
            } catch (error) {
                errorDiv.textContent = 'Error submitting review: ' + error.message;
                errorDiv.style.display = 'block';
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
        });
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
