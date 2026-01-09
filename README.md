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
   set GROQ_API_KEY="Groq_Api_key"
   ```
   
   **On Windows (PowerShell):**
   ```powershell
   $env:GROQ_API_KEY="Groq_Api_key"
   ```
   
   **On Mac/Linux:**
   ```bash
   export GROQ_API_KEY="Groq_Api_key"
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
   GROQ_API_KEY="Groq_Api_key"
   ```

5. **Run the backend server**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   * Running on https://fynd-ai-assessment.onrender.com/health
   ```
   
   This means your API server is running! Keep this terminal window open.

**Step 2: Setup Frontend**

 You should see:
   ```
   * Running on [https://fynd-ai-assessment.onrender.com/health](https://fynd-ai-assessment-hazel.vercel.app/)

## 🚀 Deployment


**GitHub Repository**: [https://github.com/shiv4321/fynd-ai-assessment]
**Report PDF**: [Your Report PDF Link]
**User Dashboard URL**: [https://fynd-ai-assessment-hazel.vercel.app/]

**Admin Dashboard URL**: [https://fynd-ai-assessment-kyvp.vercel.app/]
