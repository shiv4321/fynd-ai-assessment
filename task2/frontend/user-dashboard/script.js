// User Dashboard JavaScript
// Handles form submission and interaction with backend API

// IMPORTANT: Update this URL to your deployed backend URL after deployment
// For local development, use: http://localhost:5000
const API_BASE_URL = 'http://localhost:5000';

// Get DOM elements
const reviewForm = document.getElementById('reviewForm');
const submitBtn = document.getElementById('submitBtn');
const reviewTextarea = document.getElementById('review');
const charCount = document.getElementById('charCount');
const ratingText = document.getElementById('ratingText');
const responseContainer = document.getElementById('responseContainer');
const errorContainer = document.getElementById('errorContainer');
const loading = document.getElementById('loading');
const aiResponseDiv = document.getElementById('aiResponse');
const errorMessage = document.getElementById('errorMessage');

// Track selected rating
let selectedRating = null;

// Rating text descriptions
const ratingDescriptions = {
    1: "⭐ Poor",
    2: "⭐⭐ Fair",
    3: "⭐⭐⭐ Good",
    4: "⭐⭐⭐⭐ Very Good",
    5: "⭐⭐⭐⭐⭐ Excellent"
};

// Character counter for textarea
reviewTextarea.addEventListener('input', function() {
    const count = this.value.length;
    charCount.textContent = count;
    
    if (count > 1900) {
        charCount.style.color = '#f44336';
    } else {
        charCount.style.color = '#888';
    }
});

// Star rating selection
const ratingInputs = document.querySelectorAll('input[name="rating"]');
ratingInputs.forEach(input => {
    input.addEventListener('change', function() {
        selectedRating = parseInt(this.value);
        ratingText.textContent = ratingDescriptions[selectedRating];
        ratingText.style.color = '#667eea';
        ratingText.style.fontWeight = '600';
    });
});

// Form submission handler
submitBtn.addEventListener('click', async function(e) {
    e.preventDefault();
    
    // Validate rating selection
    if (!selectedRating) {
        showError('Please select a rating');
        return;
    }
    
    const reviewText = reviewTextarea.value.trim();
    
    // Show loading state
    showLoading();
    
    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/api/submit-review`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                rating: selectedRating,
                review: reviewText
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show success response
            showSuccess(data.ai_response);
        } else {
            // Show error message
            showError(data.message || 'Failed to submit review. Please try again.');
        }
        
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('Unable to connect to the server. Please check your connection and try again.');
    }
});

// Submit another review button
document.getElementById('submitAnother').addEventListener('click', function() {
    resetForm();
});

// Try again button
document.getElementById('tryAgain').addEventListener('click', function() {
    hideError();
});

// Helper functions
function showLoading() {
    reviewForm.style.display = 'none';
    responseContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    loading.style.display = 'block';
    submitBtn.disabled = true;
}

function hideLoading() {
    loading.style.display = 'none';
}

function showSuccess(aiResponse) {
    hideLoading();
    reviewForm.style.display = 'none';
    errorContainer.style.display = 'none';
    responseContainer.style.display = 'block';
    aiResponseDiv.textContent = aiResponse;
}

function showError(message) {
    hideLoading();
    reviewForm.style.display = 'block';
    responseContainer.style.display = 'none';
    errorContainer.style.display = 'block';
    errorMessage.textContent = message;
    submitBtn.disabled = false;
}

function hideError() {
    errorContainer.style.display = 'none';
    reviewForm.style.display = 'block';
}

function resetForm() {
    // Reset form fields
    selectedRating = null;
    reviewTextarea.value = '';
    charCount.textContent = '0';
    ratingText.textContent = 'Select a rating';
    ratingText.style.color = '#666';
    ratingText.style.fontWeight = 'normal';
    
    // Uncheck all radio buttons
    ratingInputs.forEach(input => {
        input.checked = false;
    });
    
    // Show form, hide response
    responseContainer.style.display = 'none';
    errorContainer.style.display = 'none';
    reviewForm.style.display = 'block';
    submitBtn.disabled = false;
}