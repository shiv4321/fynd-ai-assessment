# Task 2: Two-Dashboard AI Feedback System

A production-style web application with separate User and Admin dashboards for collecting and managing customer reviews with AI-powered insights.

## 🏗️ System Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  User Dashboard │         │ Admin Dashboard │
│   (Frontend)    │         │   (Frontend)    │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │      HTTP Requests        │
         │      (JSON payloads)      │
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Flask Backend API   │
         │  ┌─────────────────┐  │
         │  │  app.py         │  │
         │  │  (REST API)     │  │
         │  └────────┬────────┘  │
         │           │           │
         │  ┌────────▼────────┐  │
         │  │  llm_service.py │  │
         │  │  (Groq API)     │  │
         │  └────────┬────────┘  │
         │           │           │
         │  ┌────────▼────────┐  │
         │  │   models.py     │  │
         │  │  (Data Storage) │  │
         │  └─────────────────┘  │
         └───────────────────────┘
```

## 📂 Directory Structure

```
task2/
├── backend/
│   ├── app.py              # Main Flask application with API endpoints
│   ├── models.py           # Data models (Submission, SubmissionStore)
│   ├── llm_service.py      # LLM integration service for AI features
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables (create this)
│
└── frontend/
    ├── user-dashboard/
    │   ├── index.html     # User interface structure
    │   ├── style.css      # User interface styling
    │   └── script.js      # User interface logic
    │
    └── admin-dashboard/
        ├── index.html     # Admin interface structure
        ├── style.css      # Admin interface styling
        └── script.js      # Admin interface logic
```

## 🔧 Component Details

### Backend Components

#### 1. app.py - Flask API Server
**Purpose**: Main application server that handles HTTP requests

**Key Endpoints**:
- `GET /health` - Health check
- `POST /api/submit-review` - Submit new review
- `GET /api/submissions` - Get all submissions
- `GET /api/analytics` - Get analytics data

**Technologies**:
- **Flask**: Python web framework for building APIs
- **Flask-CORS**: Enables cross-origin requests (allows frontend to communicate with backend even when on different domains)

**How it works**:
1. Receives HTTP requests from frontend dashboards
2. Validates incoming data (rating, review text)
3. Handles edge cases (empty reviews, long reviews)
4. Calls LLM service for AI processing
5. Stores data using SubmissionStore
6. Returns JSON responses

#### 2. llm_service.py - AI Integration
**Purpose**: Manages all interactions with Groq LLM API

**Key Methods**:
- `generate_user_response()` - Creates personalized response for users
- `generate_summary()` - Summarizes reviews for admins
- `generate_recommendations()` - Suggests action items

**How LLMs are used**:
- **User Response**: Acknowledges feedback with empathy based on rating
- **Summary**: Extracts key points from review for quick admin overview
- **Recommendations**: Analyzes review to suggest specific business actions

**Error Handling**:
- Catches API failures gracefully
- Provides fallback messages if LLM is unavailable
- Includes retry logic for transient failures

#### 3. models.py - Data Management
**Purpose**: Defines data structures and storage

**Classes**:
- `Submission`: Represents a single review with all metadata
- `SubmissionStore`: In-memory storage for submissions

**Data Structure**:
```python
{
    "id": "unique-uuid",
    "rating": 1-5,
    "review": "user review text",
    "ai_response": "AI response shown to user",
    "summary": "AI summary for admin",
    "recommended_actions": "AI recommendations",
    "timestamp": "ISO format datetime"
}
```

**Why In-Memory Storage?**
- Simplest to implement and deploy
- No database setup required
- Sufficient for demo/assessment purposes
- Data persists during server runtime
- Note: For production, use PostgreSQL/MongoDB

### Frontend Components

#### User Dashboard
**Purpose**: Public-facing interface for customers to submit reviews

**Features**:
- Interactive 5-star rating selector
- Text area for detailed review (2000 char limit)
- Character counter
- Real-time form validation
- Loading indicator during submission
- AI-generated response display
- Error handling and retry

**User Flow**:
1. User selects star rating (required)
2. User writes review (optional)
3. Clicks "Submit Review"
4. Loading spinner appears
5. Backend processes and generates AI response
6. Success screen shows AI response
7. Option to submit another review

**Technologies**:
- HTML5 for structure
- CSS3 for styling (gradient backgrounds, animations)
- Vanilla JavaScript for interactivity
- Fetch API for HTTP requests

#### Admin Dashboard
**Purpose**: Internal interface for staff to view and analyze reviews

**Features**:
- Real-time statistics (total reviews, average rating)
- Rating distribution visualization (bar chart)
- Filter reviews by star rating
- Detailed submission cards showing:
  - User rating and review
  - AI response sent to user
  - AI-generated summary
  - AI-recommended actions
- Auto-refresh every 30 seconds
- Manual refresh button
- Responsive design

**Admin Flow**:
1. Dashboard loads and fetches all submissions
2. Analytics calculated and displayed
3. Submissions listed (newest first)
4. Admin can filter by rating
5. Auto-refresh keeps data current
6. Each submission shows full AI analysis

**Technologies**:
- HTML5, CSS3, JavaScript
- CSS Grid for responsive layout
- Fetch API for backend communication
- SetInterval for auto-refresh

## 🔄 Data Flow

### Review Submission Flow

```
User Action
    ↓
[User Dashboard]
Select rating + Write review
    ↓
[Frontend Validation]
Check rating exists
    ↓
[HTTP POST Request]
/api/submit-review
{rating: 4, review: "text"}
    ↓
[Backend API - app.py]
Validate & sanitize data
    ↓
[LLM Service]
Generate 3 AI outputs:
- User response
- Summary
- Recommendations
    ↓
[Data Storage]
Store in SubmissionStore
    ↓
[HTTP Response]
{success: true, ai_response: "..."}
    ↓
[User Dashboard]
Display AI response
```

### Admin Dashboard Flow

```
Page Load
    ↓
[Admin Dashboard]
Initialize & load data
    ↓
[HTTP GET Requests]
/api/submissions
/api/analytics
    ↓
[Backend API]
Retrieve from SubmissionStore
Calculate analytics
    ↓
[HTTP Response]
{submissions: [...], analytics: {...}}
    ↓
[Admin Dashboard]
Render submissions & charts
Update every 30 seconds
```

## 🚀 Local Development

### Starting the Backend

```bash
# Navigate to backend
cd task2/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with API key
echo "GROQ_API_KEY=your_key" > .env

# Run server
python app.py
```

Server runs on: `http://localhost:5000`

### Starting the Frontends

**User Dashboard:**
```bash
cd task2/frontend/user-dashboard
python -m http.server 8000
```
Access: `http://localhost:8000`

**Admin Dashboard:**
```bash
cd task2/frontend/admin-dashboard
python -m http.server 8001
```
Access: `http://localhost:8001`

## 📊 API Schema Documentation

### Submit Review Endpoint

**Request:**
```
POST /api/submit-review
Content-Type: application/json

{
  "rating": 4,              // Required: integer 1-5
  "review": "Great service" // Optional: string, max 2000 chars
}
```

**Success Response:**
```
Status: 201 Created
Content-Type: application/json

{
  "success": true,
  "message": "Review submitted successfully",
  "ai_response": "Thank you for your positive feedback! We're delighted to hear about your great experience.",
  "submission_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error Response:**
```
Status: 400 Bad Request

{
  "success": false,
  "message": "Rating must be between 1 and 5"
}
```

### Get Submissions Endpoint

**Request:**
```
GET /api/submissions
```

**Response:**
```
Status: 200 OK

{
  "success": true,
  "count": 10,
  "submissions": [
    {
      "id": "uuid",
      "rating": 5,
      "review": "Excellent!",
      "ai_response": "Thank you...",
      "summary": "Customer extremely satisfied",
      "recommended_actions": "1. Recognize staff\n2. Share feedback",
      "timestamp": "2024-01-08T10:30:00Z"
    }
  ]
}
```

### Get Analytics Endpoint

**Request:**
```
GET /api/analytics
```

**Response:**
```
Status: 200 OK

{
  "success": true,
  "analytics": {
    "total_submissions": 25,
    "rating_distribution": {
      "1": 2,
      "2": 3,
      "3": 5,
      "4": 8,
      "5": 7
    },
    "average_rating": 3.8
  }
}
```

## 🛡️ Error Handling

### Backend Error Handling

**Empty Reviews:**
- Accepted and processed
- Stored as "[No review text provided]"
- AI still generates appropriate response

**Long Reviews:**
- Truncated to 2000 characters
- Appends "..." to indicate truncation
- Full processing continues normally

**LLM API Failures:**
- Caught and logged
- Fallback messages provided
- User experience not interrupted
- Example fallback: "Thank you for your feedback! We've received your review and our team will look into it."

**Invalid Ratings:**
- Validated to be 1-5
- Clear error message returned
- Form not processed

### Frontend Error Handling

**Network Errors:**
- Caught in try-catch blocks
- User-friendly error messages
- Retry button provided

**API Failures:**
- Displays error from backend
- Allows user to try again
- Form data preserved

**Loading States:**
- Spinner shown during processing
- Submit button disabled
- Prevents duplicate submissions

## 🎨 Design Decisions

### Why Flask?
- Lightweight and simple for small APIs
- Easy to deploy on platforms like Render
- Excellent for RESTful APIs
- Strong ecosystem and documentation

### Why Separate HTML/CSS/JS?
- Clear separation of concerns
- Easy to understand and modify
- No build tools required
- Simple deployment to Vercel/Netlify

### Why In-Memory Storage?
- Simplest implementation
- No database setup
- Faster development
- Sufficient for assessment scope
- Easy to replace with database later

### Why Groq API?
- Very fast response times
- Free tier available
- Good model quality (Llama 3.1)
- Simple API interface

## 🚀 Deployment

### Backend (Render)

1. Push code to GitHub
2. Create Render account
3. New Web Service from repo
4. Configure:
   - Root: `task2/backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
5. Add environment variable: `GROQ_API_KEY`
6. Deploy

### Frontend (Vercel)

1. Update `API_BASE_URL` in both script.js files
2. Install Vercel CLI: `npm install -g vercel`
3. Deploy User Dashboard:
   ```bash
   cd task2/frontend/user-dashboard
   vercel
   ```
4. Deploy Admin Dashboard:
   ```bash
   cd task2/frontend/admin-dashboard
   vercel
   ```

## ✅ Testing Checklist

- [ ] Backend starts without errors
- [ ] Health endpoint returns 200
- [ ] Can submit review with rating only
- [ ] Can submit review with rating + text
- [ ] Empty review handled correctly
- [ ] Long review (2000+ chars) handled
- [ ] Invalid rating rejected
- [ ] User receives AI response
- [ ] Admin dashboard shows submission
- [ ] Analytics update correctly
- [ ] Filter by rating works
- [ ] Auto-refresh functions
- [ ] Manual refresh works
- [ ] All deployed URLs accessible

## 🔮 Future Enhancements

(NOT included in current scope - for reference only)

- Database integration (PostgreSQL)
- User authentication
- Email notifications
- Export to CSV functionality
- Advanced analytics (trends, sentiment over time)
- Multi-language support
- Reply to reviews feature
- Review moderation queue

## 📝 Notes

- System handles concurrent requests safely
- Rate limiting recommended for production
- Consider caching for better performance
- Monitor LLM API costs in production
- Implement proper logging for debugging