# 🚀 AI Resume Matcher

A full-stack platform powered by **FastAPI** that intelligently matches uploaded resumes to job descriptions using both **keyword overlap** and **AI-driven semantic similarity**.

Ideal for:
- 🧑‍💻 Job seekers wanting to tailor their resumes
- 🧑‍💼 Recruiters managing large pools of candidates
- 📊 HR platforms automating resume-job relevance scoring

---

## ⚙️ Tech Stack

**Backend:** FastAPI, SQLAlchemy (Async), SQL (PostgreSQL)\
**NLP:** PyMuPDF for PDF parsing, custom AI-based similarity scoring\
**Frontend:** (Optional, connect your own React/Next.js client)\
**ORM:** Async SQLAlchemy

---

## 🔑 Features

### 🗂 Upload Resumes
- Accepts `.pdf` files
- Extracts and stores text in database

### 📄 Match Job Descriptions
- Input a job description
- Returns ranked similarity scores for all stored resumes

### 🤖 AI-Based Matching
- Uses a custom similarity algorithm for semantic scoring
- Supports direct one-to-one resume vs job description scoring

### 🔄 Auto Update
- Re-evaluates all stored resumes whenever a new job description is submitted

---

## 🔌 API Endpoints

### `POST /upload_resume`
**Upload a PDF resume**  
Returns extracted text and stores the data.

### `POST /match_job`
**Submit a job description**  
Returns similarity scores for each stored resume.

### `POST /match_resume`
**Submit one resume and one job description**  
Returns an AI-driven similarity score.

### `GET /`
Health check endpoint to confirm the API is live.

---

## 🚀 Getting Started

```bash
# Clone and enter the project
git clone https://github.com/drumin4/job_application_api
cd resume-matcher

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn main:app --reload
```

---

## 🧪 Sample Request

```http
POST /match_job
Content-Type: application/json

{
  "job_description": "Looking for a Python developer with experience in FastAPI, SQLAlchemy and RESTful APIs."
}
```

---

## 🌍 Deployment Options

Can be deployed to:
- 🟣 Render
- 🟢 Railway
- 🟠 Fly.io
- 🌐 Docker (optional)

Frontend (if added) can be hosted on:
- ⚡ Vercel
- 🚀 Netlify

---

## 📌 To-Do / Future Enhancements

- [ ] DOCX resume parsing
- [ ] User accounts and authentication
- [ ] Resume editing & deletion
- [ ] Enhanced semantic matching with SBERT or OpenAI Embeddings
- [ ] Suggest missing keywords from job descriptions

---

## 👨‍💻 Author

Made with ❤️ using Python, FastAPI, and a passion for clean automation.  
Let the code speak for your skills before you do.
