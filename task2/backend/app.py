"""
Backend API for Two-Dashboard AI Feedback System
This Flask application provides REST APIs for both User and Admin dashboards.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import json
from llm_service import LLMService
from models import Submission, SubmissionStore

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for cross-origin requests from frontend dashboards
# CORS (Cross-Origin Resource Sharing) allows the frontend (HTML/JS) to make 
# requests to this backend API even if they're hosted on different domains
CORS(app)

# Initialize services
llm_service = LLMService(api_key=os.environ.get("GROQ_API_KEY"))
submission_store = SubmissionStore()

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns: JSON with status message
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/submit-review', methods=['POST'])
def submit_review():
    """
    User Dashboard Endpoint: Submit a new review
    
    Expected JSON Schema:
    {
        "rating": <number 1-5>,
        "review": <string>
    }
    
    Returns JSON Schema:
    {
        "success": <boolean>,
        "message": <string>,
        "ai_response": <string>,
        "submission_id": <string>
    }
    """
    try:
        # Parse request data
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400
        
        # Extract and validate rating
        rating = data.get('rating')
        if rating is None:
            return jsonify({
                "success": False,
                "message": "Rating is required"
            }), 400
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({
                    "success": False,
                    "message": "Rating must be between 1 and 5"
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Invalid rating format"
            }), 400
        
        # Extract review text
        review_text = data.get('review', '').strip()
        
        # Handle empty reviews - still process but note it's empty
        if not review_text:
            review_text = "[No review text provided]"
        
        # Handle long reviews - truncate if necessary
        MAX_REVIEW_LENGTH = 2000
        if len(review_text) > MAX_REVIEW_LENGTH:
            review_text = review_text[:MAX_REVIEW_LENGTH] + "..."
        
        # Generate AI response for user
        try:
            ai_response = llm_service.generate_user_response(rating, review_text)
        except Exception as llm_error:
            # Handle LLM failure gracefully
            print(f"LLM Error in user response: {llm_error}")
            ai_response = "Thank you for your feedback! We've received your review and our team will look into it."
        
        # Generate admin-facing summary and recommendations
        try:
            summary = llm_service.generate_summary(review_text, rating)
            recommended_actions = llm_service.generate_recommendations(review_text, rating)
        except Exception as llm_error:
            # Handle LLM failure gracefully for admin data
            print(f"LLM Error in admin data: {llm_error}")
            summary = "Review received. Manual review recommended."
            recommended_actions = "Please review manually due to processing error."
        
        # Create submission object
        submission = Submission(
            rating=rating,
            review=review_text,
            ai_response=ai_response,
            summary=summary,
            recommended_actions=recommended_actions
        )
        
        # Store submission
        submission_id = submission_store.add_submission(submission)
        
        # Return success response
        return jsonify({
            "success": True,
            "message": "Review submitted successfully",
            "ai_response": ai_response,
            "submission_id": submission_id
        }), 201
        
    except Exception as e:
        # Catch any unexpected errors
        print(f"Error in submit_review: {e}")
        return jsonify({
            "success": False,
            "message": "An error occurred while processing your review. Please try again."
        }), 500


@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """
    Admin Dashboard Endpoint: Get all submissions
    
    Returns JSON Schema:
    {
        "success": <boolean>,
        "count": <number>,
        "submissions": [
            {
                "id": <string>,
                "rating": <number>,
                "review": <string>,
                "ai_response": <string>,
                "summary": <string>,
                "recommended_actions": <string>,
                "timestamp": <string ISO format>
            }
        ]
    }
    """
    try:
        submissions = submission_store.get_all_submissions()
        
        return jsonify({
            "success": True,
            "count": len(submissions),
            "submissions": submissions
        }), 200
        
    except Exception as e:
        print(f"Error in get_submissions: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve submissions"
        }), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Admin Dashboard Endpoint: Get analytics summary
    
    Returns JSON Schema:
    {
        "success": <boolean>,
        "analytics": {
            "total_submissions": <number>,
            "rating_distribution": {
                "1": <number>,
                "2": <number>,
                "3": <number>,
                "4": <number>,
                "5": <number>
            },
            "average_rating": <number>
        }
    }
    """
    try:
        submissions = submission_store.get_all_submissions()
        
        # Calculate rating distribution
        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_ratings = 0
        
        for submission in submissions:
            rating = submission['rating']
            rating_counts[rating] += 1
            total_ratings += rating
        
        # Calculate average rating
        avg_rating = total_ratings / len(submissions) if len(submissions) > 0 else 0
        
        analytics = {
            "total_submissions": len(submissions),
            "rating_distribution": rating_counts,
            "average_rating": round(avg_rating, 2)
        }
        
        return jsonify({
            "success": True,
            "analytics": analytics
        }), 200
        
    except Exception as e:
        print(f"Error in get_analytics: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve analytics"
        }), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    # Check for API key
    if not os.environ.get("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY environment variable not set!")
    
    # Run the app
    # For local development, use debug=True
    # For production, debug should be False
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)