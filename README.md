# Fynd AI Intern Assessment 2.0

This repository contains the complete solution for the Fynd AI Internship Take-Home Assessment, consisting of two main tasks:
- **Task 1**: Rating prediction via LLM prompting
- **Task 2**: Two-dashboard AI feedback system

## 📁 Project Structure

```
fynd-ai-assessment/
├── task1/
│   └── rating_prediction.ipynb       # Jupyter notebook for Task 1
├── task2/
│   ├── backend/
│   │   ├── app.py                    # Flask backend API
│   │   ├── models.py                 # Data models and storage
│   │   ├── llm_service.py           # LLM integration service
│   │   ├── requirements.txt          # Python dependencies
│   │   └── .env                      # Environment variables (create this)
│   ├── frontend/
│   │   ├── user-dashboard/          # Public user interface
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   └── admin-dashboard/         # Internal admin interface
│   │       ├── index.html
│   │       ├── style.css
│   │       └── script.js
│   └── README.md
├── .gitignore
└── README.md
```

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- VS Code or any code editor
- Groq API key (already provided)

### Task 1: Rating Prediction

**What is Jupyter Notebook?**
A Jupyter notebook is an interactive document that combines code, text, and visualizations. It runs Python code in cells that you can execute one at a time.

**Setup & Execution:**

1. **Install Jupyter**
   ```bash
   pip install jupyter notebook kagglehub groq pandas numpy
   ```

2. **Set Environment Variable**
   
   **On Windows (Command Prompt):**
   ```cmd
   set GROQ_API_KEY=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
   ```
   
   **On Windows (PowerShell):**
   ```powershell
   $env:GROQ_API_KEY="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"
   ```
   
   **On Mac/Linux:**
   ```bash
   export GROQ_API_KEY=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
   ```

3. **Run the Notebook**
   ```bash
   cd task1
   jupyter notebook rating_prediction.ipynb
   ```
   
   This will open your web browser. Click on the notebook file and run all cells using "Cell > Run All"

4. **Expected Results**
   - The notebook will evaluate 3 different prompting approaches
   - It will generate a comparison table showing accuracy and JSON validity
   - Sample predictions will be displayed
   - The entire process takes approximately 10-15 minutes due to API calls

### Task 2: Two-Dashboard System

**Architecture Overview:**
- **Backend**: Flask API server that handles requests from both dashboards
- **Frontend**: Two separate HTML/CSS/JS dashboards (User & Admin)
- **LLM Service**: Groq API integration for AI responses
- **Storage**: In-memory storage (data persists during runtime only)

**Key Technologies Explained:**

1. **Flask**: A lightweight Python web framework for building APIs
2. **Flask-CORS**: Enables Cross-Origin Resource Sharing (allows frontend to talk to backend)
3. **Groq**: Fast LLM API service (similar to OpenAI but faster)
4. **REST API**: Communication protocol between frontend and backend using JSON

#### Local Development Setup

**Step 1: Setup Backend**

1. **Navigate to backend directory**
   ```bash
   cd task2/backend
   ```

2. **Create and activate virtual environment**
   
   **What is a virtual environment?**
   It's an isolated Python environment that keeps dependencies separate from your system Python.
   
   **On Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **On Mac/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   You'll see `(venv)` in your terminal when activated.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   
   Create a file named `.env` in the `backend` folder with:
   ```
   GROQ_API_KEY=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
   ```

5. **Run the backend server**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   * Running on http://0.0.0.0:5000
   ```
   
   This means your API server is running! Keep this terminal window open.

**Step 2: Setup Frontend**

**What is a static file server?**
HTML/CSS/JS files need to be served through a web server to work properly with APIs and avoid security restrictions.

1. **Open a NEW terminal window** (keep backend running in the first one)

2. **For User Dashboard:**
   ```bash
   cd task2/frontend/user-dashboard
   
   # On Windows (using Python)
   python -m http.server 8000
   
   # On Mac/Linux
   python3 -m http.server 8000
   ```
   
   Open browser: `http://localhost:8000`

3. **For Admin Dashboard (in ANOTHER new terminal):**
   ```bash
   cd task2/frontend/admin-dashboard
   
   # On Windows
   python -m http.server 8001
   
   # On Mac/Linux
   python3 -m http.server 8001
   ```
   
   Open browser: `http://localhost:8001`

**Testing the System:**

1. Open User Dashboard (`http://localhost:8000`)
2. Select a star rating (1-5)
3. Write a review
4. Click "Submit Review"
5. You should see an AI-generated response
6. Open Admin Dashboard (`http://localhost:8001`)
7. Your submission should appear with AI summary and recommendations
8. The dashboard auto-refreshes every 30 seconds

## 📊 API Endpoints

### POST /api/submit-review
Submit a new review

**Request:**
```json
{
  "rating": 4,
  "review": "Great service!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Review submitted successfully",
  "ai_response": "Thank you for your positive feedback!",
  "submission_id": "uuid-here"
}
```

### GET /api/submissions
Retrieve all submissions

**Response:**
```json
{
  "success": true,
  "count": 10,
  "submissions": [...]
}
```

### GET /api/analytics
Get analytics summary

**Response:**
```json
{
  "success": true,
  "analytics": {
    "total_submissions": 10,
    "rating_distribution": {...},
    "average_rating": 4.2
  }
}
```

## 🚀 Deployment Guide

### Backend Deployment (Render)

**Why Render?**
Render provides free hosting for backend services with automatic HTTPS and easy environment variable management.

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   - **Name**: `fynd-backend` (or your choice)
   - **Root Directory**: `task2/backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Add Environment Variables**
   - Go to "Environment" tab
   - Add: `GROQ_API_KEY` = `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`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL (e.g., `https://fynd-backend.onrender.com`)

### Frontend Deployment (Vercel)

**Why Vercel?**
Vercel specializes in hosting static websites (HTML/CSS/JS) with instant global CDN and automatic HTTPS.

**User Dashboard:**

1. **Update API URL**
   - Open `task2/frontend/user-dashboard/script.js`
   - Change `API_BASE_URL` to your Render backend URL:
     ```javascript
     const API_BASE_URL = 'https://fynd-backend.onrender.com';
     ```

2. **Deploy to Vercel**
   - Install Vercel CLI: `npm install -g vercel`
   - Navigate to: `cd task2/frontend/user-dashboard`
   - Run: `vercel`
   - Follow prompts (press Enter for defaults)
   - Copy the deployment URL

**Admin Dashboard:**

1. **Update API URL**
   - Open `task2/frontend/admin-dashboard/script.js`
   - Change `API_BASE_URL` to your Render backend URL

2. **Deploy**
   - Navigate to: `cd task2/frontend/admin-dashboard`
   - Run: `vercel`
   - Copy the deployment URL

**Alternative: Manual Vercel Deployment**

If you prefer using the Vercel website:
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Set root directory to `task2/frontend/user-dashboard` (or `admin-dashboard`)
5. Click "Deploy"

## ✅ Verification Checklist

- [ ] Task 1 notebook runs successfully and generates comparison table
- [ ] Backend API runs locally on port 5000
- [ ] User Dashboard loads and can submit reviews
- [ ] Admin Dashboard loads and displays submissions
- [ ] Backend is deployed on Render and accessible
- [ ] User Dashboard is deployed on Vercel
- [ ] Admin Dashboard is deployed on Vercel
- [ ] All deployed URLs are functional
- [ ] Data persists across page refreshes (during server runtime)

## 🎯 Key Features Implemented

### Task 1
✅ 3 different prompting approaches
✅ JSON structured output validation
✅ Accuracy and MAE evaluation
✅ Comparison table and discussion
✅ Sample predictions display

### Task 2
✅ User-facing review submission form
✅ 5-star rating selection
✅ AI-generated user responses
✅ Admin dashboard with submissions list
✅ AI-generated summaries
✅ AI-recommended actions
✅ Analytics (total reviews, rating distribution, average)
✅ Filter by rating functionality
✅ Auto-refresh every 30 seconds
✅ Error handling (empty reviews, long reviews, API failures)
✅ Server-side LLM calls only
✅ Explicit JSON schemas for API
✅ Persistent data storage (in-memory)
✅ Fully deployed on free platforms

## 🛠️ Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check if port 5000 is available
- Verify GROQ_API_KEY is set correctly
- Try: `pip install --upgrade -r requirements.txt`

### Frontend can't connect to backend
- Check if backend is running (terminal should show Flask server running)
- Verify API_BASE_URL in script.js matches your backend URL
- Check browser console for CORS errors
- Try accessing `http://localhost:5000/health` directly in browser

### Task 1 notebook fails
- Ensure GROQ_API_KEY environment variable is set
- Check internet connection for Kaggle dataset download
- Reduce sample size if running into rate limits
- Try restarting notebook kernel

### Deployment issues
- Render: Check logs in Render dashboard for errors
- Vercel: Check deployment logs in Vercel dashboard
- Ensure environment variables are set on hosting platform
- Verify build commands are correct

## 📝 Notes

- The system uses in-memory storage, so data will be lost when the backend server restarts
- For production use, implement database storage (PostgreSQL, MongoDB, etc.)
- Rate limiting is implemented in the LLM service to avoid API throttling
- Frontend includes loading states and error handling for better UX

## 📧 Submission Links

**GitHub Repository**: [Your GitHub URL]
**Report PDF**: [Your Report PDF Link]
**User Dashboard URL**: [Your Deployed User Dashboard]
**Admin Dashboard URL**: [Your Deployed Admin Dashboard]