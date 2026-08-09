import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from parser import extract_text
from ats import compare_resume_with_jd
from ai import get_ai_feedback
from database import engine, Base, get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
RESUME_FOLDER = "uploads/resumes"
JD_FOLDER = "uploads/job_descriptions"

os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(JD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Backend Running Successfully"}


@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    file_path = os.path.join(RESUME_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract resume text
    resume_text = extract_text(file_path)

    # Compare resume with job description
    result = compare_resume_with_jd(
        resume_text,
        job_description
    )

    # AI Feedback
    try:
        ai_feedback = get_ai_feedback(
            resume_text,
            job_description
        )
    except Exception as e:
        ai_feedback = f"AI Error: {str(e)}"

    # Save Resume
    db_resume = models.Resume(
        filename=file.filename,
        raw_text=resume_text,
        ats_score=result["match_percentage"],
        matched_skills=result["matched_skills"]
    )

    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    return {
        "id": db_resume.id,
        "filename": db_resume.filename,
        "ATS Score": result["match_percentage"],
        "Matched Skills": result["matched_skills"],
        "Missing Skills": result["missing_skills"],
        "AI Feedback": ai_feedback,
        "Preview": resume_text[:500]
    }

@app.post("/upload-jd")
async def upload_job_description(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(JD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    jd_text = extract_text(file_path)

    db_jd = models.JobDescription(
        filename=file.filename,
        raw_text=jd_text
    )

    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)

    return {
        "id": db_jd.id,
        "filename": db_jd.filename,
        "job_description": db_jd.raw_text
    }

@app.post("/match")
async def match_resume(
    resume_id: int = Form(...),
    jd_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Get resume
    db_resume = db.query(models.Resume).filter(
        models.Resume.id == resume_id
    ).first()

    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume ID not found.")

    # Get job description
    db_jd = db.query(models.JobDescription).filter(
        models.JobDescription.id == jd_id
    ).first()

    if not db_jd:
        raise HTTPException(status_code=404, detail="Job Description not found.")

    # Compare resume with job description
    result = compare_resume_with_jd(
        db_resume.raw_text,
        db_jd.raw_text
    )

    # AI Feedback
    try:
        ai_feedback = get_ai_feedback(
            db_resume.raw_text,
            db_jd.raw_text
        )
    except Exception as e:
        ai_feedback = f"AI Error: {str(e)}"

    # Save match
    db_match = models.JobMatch(
        resume_id=db_resume.id,
        jd_id=db_jd.id,
        match_percentage=result["match_percentage"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        ai_feedback=ai_feedback
    )

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return {
        "match_id": db_match.id,
        "resume_id": db_match.resume_id,
        "jd_id": db_match.jd_id,
        "match_percentage": db_match.match_percentage,
        "matched_skills": db_match.matched_skills,
        "missing_skills": db_match.missing_skills,
        "ai_feedback": db_match.ai_feedback
    }