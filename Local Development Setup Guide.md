# Local Development Setup Guide

## Overview

This guide provides step-by-step instructions for setting up and running the LessonPlanBuilder application on your local machine. The application consists of a Python FastAPI backend with Google GenAI SDK integration and a React frontend.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

- **Python 3.11 or higher**
  - Check version: `python3 --version`
  - Download: https://www.python.org/downloads/

- **Node.js v20 LTS** (recommended)
  - Check version: `node --version`
  - Download: https://nodejs.org/
  - Note: Node.js v24 may have compatibility issues

- **MongoDB**
  - Community Edition or MongoDB Atlas (cloud)
  - Download: https://www.mongodb.com/try/download/community

- **pip** (Python package manager)
  - Usually comes with Python
  - Check version: `pip3 --version`

- **npm** (Node package manager)
  - Comes with Node.js
  - Check version: `npm --version`

### API Keys Required

- **Google Gemini API Key**
  - Get it from: https://aistudio.google.com/app/apikey
  - Free tier available

## System Requirements

### Minimum Requirements

- **Operating System**: macOS, Linux, or Windows 10+
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB free space
- **Internet Connection**: Required for API calls and package installation

### Recommended Development Tools

- **Terminal/Command Line**: iTerm2 (macOS), Windows Terminal, or any modern terminal
- **Code Editor**: VS Code, Sublime Text, or any preferred editor
- **Browser**: Chrome, Firefox, or Safari with Developer Tools

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/LlmPoweredLessonPlanBuilder.git
cd LlmPoweredLessonPlanBuilder
```

### Step 2: Install MongoDB

#### MongoDB Local Installation

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Windows:**
- Download installer from: https://www.mongodb.com/try/download/community
- Run the installer and follow the setup wizard
- MongoDB will start as a Windows service

**Verify MongoDB is Running:**
```bash
# Check if MongoDB is listening on port 27017
lsof -i :27017  # macOS/Linux
netstat -an | find "27017"  # Windows
```

### Step 3: Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

If you encounter permission errors, use:
```bash
pip3 install --user -r requirements.txt
```

### Step 4: Install Frontend Dependencies

```bash
cd ../frontend
npm install --legacy-peer-deps
```

The `--legacy-peer-deps` flag resolves dependency conflicts.

If you encounter errors, try:
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps
```

## Configuration

### Backend Configuration

#### Step 1: Get Your Google Gemini API Key

1. Visit https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key 

#### Step 2: Generate JWT Secret

Generate a secure random string for JWT token signing:

```bash
openssl rand -hex 32
```

Or use Python:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### Step 3: Create Backend .env File

Create a file named `.env` in the `backend` directory:

```bash
cd backend
nano .env
```

Add the following content (replace placeholders with your actual values):

```env
GOOGLE_API_KEY=your-gemini-api-key-here
MONGO_URL=mongodb://localhost:27017
DB_NAME=lessonplanbuilder
JWT_SECRET=your-generated-jwt-secret-here
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

**Important Notes:**
- No spaces around `=` signs
- No comments on the same line as values
- No quotes around values unless they contain spaces

**Example with actual values:**

```env
GOOGLE_API_KEY=AIzaSyA.......
MONGO_URL=mongodb://localhost:27017
DB_NAME=lessonplanbuilder
JWT_SECRET=a7f3e9d2c1b4a8...............
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

Save and exit (Ctrl+X, then Y, then Enter in nano).

### Frontend Configuration

Create a file named `.env` in the `frontend` directory:

```bash
cd ../frontend
nano .env
```

Add the following content:

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

Save and exit.

**Important:** The variable name must be exactly `REACT_APP_BACKEND_URL`

## Running the Application

You need to run both the backend and frontend servers simultaneously. Open two terminal windows.

### Terminal 1: Start Backend Server

```bash
cd backend
uvicorn server:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The backend API is now running at: http://localhost:8000

**API Documentation:** http://localhost:8000/docs

### Terminal 2: Start Frontend Server

```bash
cd frontend
npm start
```

You should see:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://10.x.x.x:3000
```

The frontend will automatically open in your browser at: http://localhost:3000

## Testing

### Test 1: Verify Backend is Running

Open your browser and visit:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/api/options - Should return JSON with options

### Test 2: Run Integration Tests

From the repository root:

```bash
python3 test_genai_integration.py
```

Expected output:
```
============================================================
GOOGLE GENAI SDK - LOCAL SERVER TEST
============================================================
Testing: http://localhost:8000

[PASS] Options endpoint accessible
[PASS] Bloom's Taxonomy levels: 6
[PASS] AQF levels: 10
[PASS] Lesson durations: 7
[PASS] Signup successful
[PASS] Lesson plan generated successfully!

============================================================
TEST SUMMARY
============================================================
Tests Passed: 7/7
Success Rate: 100.0%

All tests passed! Google GenAI SDK is working correctly.
```

### Test 3: Run Full Test Suite

```bash
python3 test_local_with_auth.py
```

### Test 4: Manual Testing via Frontend

1. Open http://localhost:3000
2. Click "Sign Up"
3. Fill in the registration form
4. Create an account
5. Upload a PDF course outline
6. Generate a lesson plan:
   - Enter subject name
   - Enter lecture topic
   - Enter focus topic
   - Select Bloom's taxonomy level
   - Select AQF level
   - Select lesson duration
   - Click "Generate Lesson Plan"
7. Wait for AI to generate the lesson plan
8. Download the lesson plan as PDF


## Architecture Overview

### Technology Stack

**Backend:**
- **Framework:** FastAPI (Python)
- **AI Integration:** Google GenAI SDK (Gemini 2.0 Flash)
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Tokens)
- **PDF Processing:** PyPDF2, ReportLab
- **Server:** Uvicorn (ASGI server)

**Frontend:**
- **Framework:** React 18
- **Build Tool:** Create React App with CRACO
- **HTTP Client:** Axios
- **UI Components:** Custom components with Tailwind CSS
- **Routing:** React Router v6
- **Icons:** Lucide React

### Application Flow

1. **User Registration/Login**
   - User signs up or logs in via frontend
   - Backend validates credentials and returns JWT token
   - Token stored in localStorage for subsequent requests

2. **PDF Upload**
   - User uploads course outline PDF
   - Backend extracts text using PyPDF2
   - Google GenAI SDK analyzes content and extracts:
     - Subject names
     - Lecture topics
     - Focus areas per lecture

3. **Lesson Plan Generation**
   - User fills in lesson plan parameters
   - Frontend sends authenticated request to backend
   - Backend constructs prompt with parameters
   - Google GenAI SDK (Gemini) generates lesson plan
   - Backend saves to MongoDB and returns content
   - Frontend displays generated lesson plan

4. **PDF Download**
   - User requests PDF download
   - Backend retrieves lesson plan from MongoDB
   - ReportLab generates formatted PDF
   - PDF sent to user for download

### API Endpoints

**Authentication:**
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/validate-api-key` - Validate user's API key

**Lesson Planning:**
- `GET /api/options` - Get available options (Bloom's levels, AQF levels, durations)
- `POST /api/upload-pdf` - Upload and analyze course outline PDF
- `POST /api/generate-lesson-plan` - Generate AI-powered lesson plan
- `GET /api/download-lesson-plan/{id}` - Download lesson plan as PDF

**Status:**
- `GET /api/status` - Get status checks
- `POST /api/status` - Create status check

### Environment Variables

**Backend (`backend/.env`):**
```
GOOGLE_API_KEY          - Google Gemini API key
MONGO_URL              - MongoDB connection string
DB_NAME                - MongoDB database name
JWT_SECRET             - Secret key for JWT token signing
CORS_ORIGINS           - Allowed CORS origins (comma-separated)
```

**Frontend (`frontend/.env`):**
```
REACT_APP_BACKEND_URL  - Backend API base URL
```


## Security Considerations

### For Development

- Use strong JWT secrets (32+ character random strings)
- Keep API keys in `.env` files (never commit to git)
- Use MongoDB authentication in production
- Implement rate limiting for production deployments

### For Production

- Use HTTPS for all connections
- Set specific CORS origins (not wildcards)
- Use MongoDB Atlas with IP whitelisting
- Implement proper error handling and logging
- Use environment-specific configuration
- Enable MongoDB authentication
- Use reverse proxy (nginx) in front of uvicorn
- Implement API rate limiting
- Use secure JWT secrets (64+ characters)

## Performance Optimization

### Backend

- Use connection pooling for MongoDB
- Implement caching for frequently accessed data
- Use async operations for I/O-bound tasks
- Monitor API rate limits

### Frontend

- Build production bundle: `npm run build`
- Use code splitting and lazy loading
- Implement proper error boundaries
- Optimize images and assets


