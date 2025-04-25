import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from app.database import get_db
from app.models import ResumeData
from app.resume_parser import extract_text_from_resume
from app.similarity import compute_similarity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
TEMP_FOLDER = "temp_files"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route to confirm the API is running
@app.get("/")
async def root():
    return {"message": "🚀 Job Matcher API is up and running!"}

# ✅ Request body model for /match_job
class JobDescriptionRequest(BaseModel):
    job_description: str

# ✅ Endpoint 1: Match a job description to all resumes in the database
@app.post("/match_job")
async def match_job_description(
        request: JobDescriptionRequest,
        db: AsyncSession = Depends(get_db)
):
    job_description = request.job_description

    if not job_description:
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    result = await db.execute(select(ResumeData))
    resumes = result.scalars().all()

    matches = []

    for resume in resumes:
        similarity_score = compute_similarity(resume.extracted_text, job_description)
        matches.append({
            "resume_id": resume.id,
            "match_score": round(similarity_score * 100, 2)
        })

    return matches

# ✅ Endpoint 2: AI-based matching of a single resume + job description
class MatchRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/match_resume")
async def match_resume(data: MatchRequest):
    score = compute_similarity(data.resume_text, data.job_description)
    return {"similarity_score": round(score * 100, 2)}

# ✅ Endpoint 3: Upload a resume PDF and extract text
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        contents = await file.read()
        os.makedirs(TEMP_FOLDER, exist_ok=True)
        file_path = os.path.join(TEMP_FOLDER, f"temp_{file.filename}")

        with open(file_path, "wb") as f:
            f.write(contents)

        text = extract_text_from_resume(file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the resume: {e}")

    try:
        # 🔍 Check if resume with same filename exists
        result = await db.execute(select(ResumeData).where(ResumeData.filename == file.filename))
        existing_resume = result.scalar_one_or_none()

        if existing_resume:
            # 🔁 Update extracted_text if resume exists
            existing_resume.extracted_text = text
            await db.commit()
            action = "updated"
        else:
            # ➕ Insert new resume
            new_resume = ResumeData(filename=file.filename, extracted_text=text)
            db.add(new_resume)
            await db.commit()
            action = "created"

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save resume data to database: {e}")
    finally:
        os.remove(file_path)

    return {
        "message": f"Resume successfully {action}.",
        "file_name": file.filename,
        "extracted_text": text
    }
