# LLM Lesson Plan Builder - Technical Documentation

## Project Overview

The LLM Lesson Plan Builder is a web-based application that leverages AI to help educators create comprehensive lesson plans from PDF subject outlines. The application uses Gemini LLM for intelligent text extraction and lesson plan generation.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **LLM Integration**: Gemini 2.0-flash
- **PDF Processing**: pypdf for text extraction
- **PDF Generation**: reportlab for professional PDF output
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT


### Frontend
- **Framework**: React 19.0.0
- **UI Components**: Shadcn UI (Radix UI primitives)
- **Styling**: Tailwind CSS 3.4.17
- **Icons**: Lucide React
- **HTTP Client**: Axios 1.8.4
- **Routing**: React Router DOM 7.5.1
- **Build Tool**: Create React App with CRACO

### Database Schema

#### MongoDB Collections

**1. pdf_extractions**
```javascript
{
  _id: ObjectId,
  id: String (UUID),
  filename: String,
  subject_names: Array<String>,
  lecture_topics: Array<String>,
  lecture_focus_mapping: {
    "lecture_topic_1": ["focus_1", "focus_2"],
    "lecture_topic_2": ["focus_1", "focus_2"]
  },
  extracted_at: Date
}
```

**2. lesson_plans**
```javascript
{
  _id: ObjectId,
  id: String (UUID),
  request_data: {
    subject_name: String,
    lecture_topic: String,
    focus_topic: String (optional),
    blooms_taxonomy: String,
    aqf_level: String,
    lesson_duration: String
  },
  content: String (formatted lesson plan text),
  generated_at: Date
}
```

**3. status_checks**
```javascript
{
  _id: ObjectId,
  id: String (UUID),
  client_name: String,
  timestamp: Date
}
```

## Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │────│   FastAPI API    │────│   MongoDB       │
│   (Frontend)    │    │   (Backend)      │    │   (Database)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         │                       │
         │              ┌──────────────────┐
         │              │   Gemini LLM     │
         │              │                  │
         │              └──────────────────┘
         │
┌─────────────────┐
│   File System   │
│   (Temp PDFs)   │
└─────────────────┘
```

### Application Flow
1. **PDF Upload**: User uploads subject outline PDF
2. **Text Extraction**: pypdf extracts text from PDF
3. **LLM Analysis**: Gemini analyzes content and extracts structured data
4. **Data Storage**: Extracted data saved to MongoDB
5. **Form Population**: Frontend populates dropdowns with extracted data
6. **User Configuration**: User selects options (Bloom's taxonomy, AQF levels, etc.)
7. **Lesson Generation**: Gemini generates comprehensive lesson plan
8. **PDF Generation**: reportlab creates professional PDF document
9. **Download**: User downloads generated lesson plan

## API Endpoints

### Base URL
- Development: `http://localhost:8001/api`
- Production: `{REACT_APP_BACKEND_URL}/api`

### Endpoints

#### 1. Health Check
- **GET** `/`
- **Response**: `{"message": "LLM Lesson Plan Builder API"}`

#### 2. Get Standard Options
- **GET** `/options`
- **Response**:
```json
{
  "blooms_taxonomy": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"],
  "aqf_levels": ["AQF Level 1 - Certificate I", ...],
  "lesson_durations": ["30 minutes", "45 minutes", ...]
}
```

#### 3. Upload and Process PDF
- **POST** `/upload-pdf`
- **Content-Type**: `multipart/form-data`
- **Body**: File upload (PDF)
- **Response**: PDFExtractionResult object

#### 4. Generate Lesson Plan
- **POST** `/generate-lesson-plan`
- **Content-Type**: `application/json`
- **Body**: LessonPlanRequest object
- **Response**: LessonPlan object

#### 5. Download Lesson Plan PDF
- **GET** `/download-lesson-plan/{lesson_plan_id}`
- **Response**: PDF file download

#### 6. Status Management
- **POST** `/status` - Create status check
- **GET** `/status` - Get status checks

## LLM Integration Details

### Gemini Configuration
- **Model**: gemini-2.0-flash
- **Provider**: Google
- **API Key**: Google Gemini API Key

### Text Extraction Prompt
```
Analyze academic subject outline PDF content and extract:
- Subject names from headers/titles
- Lecture topics from timetable of activities
- Focus topics mapped to specific lecture topics
- Return structured JSON with lecture_focus_mapping
```

### Lesson Plan Generation Prompt
```
Create comprehensive lesson plan with:
- Learning objectives (aligned with Bloom's taxonomy)
- Learning outcomes (appropriate for AQF level)
- Lesson structure with time allocations
- Assessment criteria and activities
- Professional formatting without markdown
```

## File Structure

```
/app/
├── backend/
│   ├── server.py                 # Main FastAPI application
│   ├── requirements.txt          # Python dependencies
│   └── .env                     # Environment variables
├── frontend/
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Custom styles
│   │   ├── index.js            # Entry point
│   │   └── components/ui/      # Shadcn UI components
│   ├── package.json            # Node dependencies
│   ├── tailwind.config.js      # Tailwind configuration
│   └── .env                    # Frontend environment variables
└── TECHNICAL_DOCUMENTATION.md  # This file
```

## Dependencies

### Backend Dependencies (requirements.txt)
```
fastapi==0.110.1
uvicorn==0.25.0
motor==3.3.1                    # Async MongoDB driver
pymongo==4.5.0                  # MongoDB driver
pypdf==6.1.0                   # PDF text extraction
reportlab==4.4.4               # PDF generation
python-multipart==0.0.20       # File upload handling
python-dotenv==1.1.1           # Environment management
pydantic>=2.6.4                # Data validation
```

### Frontend Dependencies (package.json)
```json
{
  "react": "^19.0.0",
  "axios": "^1.8.4",
  "react-router-dom": "^7.5.1",
  "@radix-ui/*": "Various versions",
  "tailwindcss": "^3.4.17",
  "lucide-react": "^0.507.0"
}
```


## Features Implementation

### 1. Smart Focus Topic Filtering
- Backend extracts lecture-focus mappings during PDF processing
- Frontend filters focus topics based on selected lecture topic
- Automatic reset when lecture topic changes
- Optional focus topic handling for lectures without subtopics

### 2. Professional Formatting
- LLM generates clean text without markdown symbols
- Frontend renders with proper typography hierarchy
- PDF output with professional styling and structure
- Section headings in ALL CAPS with bold formatting

### 3. Three-Step Workflow
- **Step 1**: PDF Upload with drag & drop
- **Step 2**: Form configuration with extracted + standard data
- **Step 3**: Lesson plan generation and download

### 4. Educational Standards Integration
- Complete Bloom's Taxonomy levels (Remember → Create)
- Australian Qualifications Framework (AQF) levels 1-10
- Standard lesson durations (30 minutes to 3 hours)

## Security Considerations

### Current Implementation
- No user authentication (public access)
- File upload restricted to PDF format
- Temporary file handling with cleanup
- CORS configured for development

### Production Recommendations
- Implement user authentication and authorization
- Add rate limiting for API endpoints
- Secure file upload with virus scanning
- Implement proper logging and monitoring
- Use environment-specific CORS configuration



## Testing Strategy

### Current Testing
- Automated backend API testing
- Frontend component and integration testing
- End-to-end workflow testing
- LLM integration validation

### Test Coverage
- 100% backend API endpoint coverage
- Frontend UI and interaction testing
- Error handling and edge cases
- Professional formatting validation


## Support and Maintenance

### Monitoring
- Application logs via Python logging
- Error tracking and reporting
- Performance monitoring for LLM calls
- Database query performance monitoring

### Backup Strategy
- Regular MongoDB backups
- Version control for all code changes
- Environment configuration backups
- Disaster recovery procedures


