
# AI-Powered Resume Intelligence & Job Matching System

An AI-powered full-stack application that analyzes PDF resumes, matches candidates with job descriptions, identifies skill gaps, and recommends learning actions to improve job readiness.

## Features

- PDF resume text extraction
- Semantic resume-to-job similarity using Sentence Transformers
- Automatic skill extraction and skill-gap analysis
- Personalized learning and project recommendations
- Ranked job-matching results
- Analysis history using SQLite
- React frontend and FastAPI backend
- Automated tests using pytest

## Tech Stack

- Frontend: React, Vite, CSS
- Backend: Python, FastAPI
- AI/NLP: Sentence Transformers, scikit-learn
- PDF Processing: PyMuPDF
- Database: SQLite, SQLAlchemy
- Testing: pytest, FastAPI TestClient

## Project Structure

```text
resume-intelligence/
├── backend/
├── frontend/
├── data/
│   └── jobs.json
├── tests/
├── README.md
└── .gitignore
```

## Requirements

- Python 3.12+
- Node.js and npm

## Run the Backend

Activate your virtual environment from the project root:

```powershell
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
python -m pip install -r backend/requirements.txt
```

Start the backend:

```powershell
python -m uvicorn main:app --reload --app-dir backend
```

Backend API documentation:

http://127.0.0.1:8000/docs

## Run the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, usually:

http://localhost:5173

## Run Tests

From the project root:

```powershell
python -m pytest tests -v
```

## Current Limitations

- Scanned PDFs requiring OCR are not supported yet.
- The included job listings are fictional sample data.
- Similarity scores are indicators of textual relevance, not probabilities of getting hired.
- Skill extraction uses a predefined vocabulary and may miss skills or context.

## Future Improvements

- Docker and Docker Compose
- Cloud deployment on AWS
- OCR support for scanned resumes
- Authentication and user accounts
- Expanded job data and skill vocabulary
- Improved upload security and API monitoring

## Disclaimer

This application is a portfolio and learning project. Its recommendations and similarity scores should not be treated as hiring decisions.
