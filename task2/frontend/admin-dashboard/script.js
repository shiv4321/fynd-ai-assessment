// Admin Dashboard JavaScript
// Handles fetching and displaying submissions with auto-refresh

// IMPORTANT: Update this URL to your deployed backend URL after deployment
// For local development, use: http://localhost:5000
const API_BASE_URL = 'https://fynd-ai-assessment.onrender.com/';

// State management
let allSubmissions = [];
let currentFilter = 'all';

// Auto-refresh interval (30 seconds)
const AUTO_REFRESH_INTERVAL = 30000;
let refreshInterval;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadSubmissions();
    setupEventListeners();
    startAutoRefresh();
});

// Setup event listeners
function setupEventListeners() {
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', function() {
        loadSubmissions();
    });

    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Update active state
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Update filter and re-render
            currentFilter = this.dataset.filter;
            renderSubmissions();
        });
    });
}

// Start auto-refresh
function startAutoRefresh() {
    refreshInterval = setInterval(() => {
        loadSubmissions(true); // Silent refresh (no loading indicator)
    }, AUTO_REFRESH_INTERVAL);
}

// Stop auto-refresh (cleanup)
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}

// Load submissions from API
async function loadSubmissions(silent = false) {
    if (!silent) {
        showLoading();
    }

    try {
        // Fetch submissions
        const submissionsResponse = await fetch(`${API_BASE_URL}/api/submissions`);
        const submissionsData = await submissionsResponse.json();

        // Fetch analytics
        const analyticsResponse = await fetch(`${API_BASE_URL}/api/analytics`);
        const analyticsData = await analyticsResponse.json();

        if (submissionsData.success) {
            allSubmissions = submissionsData.submissions;
            updateAnalytics(analyticsData.analytics);
            renderSubmissions();
        } else {
            showError('Failed to load submissions');
        }

    } catch (error) {
        console.error('Error loading submissions:', error);
        if (!silent) {
            showError('Unable to connect to the server');
        }
    } finally {
        if (!silent) {
            hideLoading();
        }
    }
}

// Update analytics display
function updateAnalytics(analytics) {
    // Update total reviews
    document.getElementById('totalReviews').textContent = analytics.total_submissions;

    // Update average rating
    document.getElementById('avgRating').textContent = analytics.average_rating.toFixed(1);

    // Update rating distribution
    const distribution = analytics.rating_distribution;
    const maxCount = Math.max(...Object.values(distribution));

    for (let rating = 1; rating <= 5; rating++) {
        const count = distribution[rating] || 0;
        const percentage = maxCount > 0 ? (count / maxCount) * 100 : 0;
        
        // Update count
        document.getElementById(`count${rating}`).textContent = count;
        
        // Update bar width
        const bar = document.querySelector(`.bar[data-rating="${rating}"]`);
        bar.style.width = `${percentage}%`;
    }
}

// Render submissions based on current filter
function renderSubmissions() {
    const container = document.getElementById('submissionsContainer');
    const emptyState = document.getElementById('emptyState');

    // Filter submissions
    let filteredSubmissions = allSubmissions;
    if (currentFilter !== 'all') {
        const filterRating = parseInt(currentFilter);
        filteredSubmissions = allSubmissions.filter(s => s.rating === filterRating);
    }

    // Show empty state if no submissions
    if (filteredSubmissions.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    // Render submission cards
    container.innerHTML = filteredSubmissions.map(submission => `
        <div class="submission-card">
            <div class="submission-header">
                <div class="rating-badge rating-${submission.rating}">
                    ${getStars(submission.rating)} ${submission.rating}/5
                </div>
                <div class="timestamp">
                    ${formatTimestamp(submission.timestamp)}
                </div>
            </div>
            
            <div class="submission-content">
                <div class="content-section">
                    <h4>📝 User Review</h4>
                    <div class="review-text">
                        ${escapeHtml(submission.review)}
                    </div>
                </div>

                <div class="content-section">
                    <h4>💬 AI Response to User</h4>
                    <div class="ai-response-text">
                        ${escapeHtml(submission.ai_response)}
                    </div>
                </div>

                <div class="content-section">
                    <h4>📊 AI Summary</h4>
                    <div class="summary-text">
                        ${escapeHtml(submission.summary)}
                    </div>
                </div>

                <div class="content-section">
                    <h4>✅ Recommended Actions</h4>
                    <div class="actions-text">
                        ${escapeHtml(submission.recommended_actions)}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Helper function to get star emoji
function getStars(rating) {
    return '⭐'.repeat(rating);
}

// Helper function to format timestamp
function formatTimestamp(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) {
        return 'Just now';
    } else if (diffMins < 60) {
        return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
        return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show loading state
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('submissionsContainer').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
}

// Hide loading state
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('submissionsContainer').style.display = 'flex';
}

// Show error (simple console log for now)
function showError(message) {
    console.error(message);
    hideLoading();

}
