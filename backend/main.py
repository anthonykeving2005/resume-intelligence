
import json
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from database import Base, SessionLocal, engine
from matching_engine import calculate_similarity
from models import Analysis
from recommendations import recommend_skills
from resume_parser import extract_resume_text
from skills import analyze_skill_gap


app = FastAPI(title="Resume Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
JOBS_FILE = Path(
    os.getenv("JOBS_FILE", str(PROJECT_ROOT / "data" / "jobs.json"))
)


def load_jobs():
    try:
        with open(JOBS_FILE, encoding="utf-8") as file:
            jobs = json.load(file)

        if not isinstance(jobs, list):
            raise ValueError("Job data must be a list.")

        return jobs

    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not load job data. Check data/jobs.json."
        ) from exc


@app.get("/")
def root():
    return {
        "message": "Resume Intelligence API",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/jobs")
def get_jobs():
    return load_jobs()


@app.post("/api/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    content = await file.read()

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Maximum PDF size is 5 MB."
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF."
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp:
            temp.write(content)
            temp_path = temp.name

        try:
            resume_text = extract_resume_text(temp_path)
        except Exception as exc:
            raise HTTPException(
                status_code=422,
                detail="Could not read this PDF. Try another text-based PDF."
            ) from exc

        if not resume_text:
            raise HTTPException(
                status_code=422,
                detail="No text found. Scanned PDF OCR is not enabled yet."
            )

        results = []

        for job in load_jobs():
            gap = analyze_skill_gap(
                resume_text,
                job["description"]
            )

            recommendations = recommend_skills(
                gap["missing_skills"]
            )

            score = calculate_similarity(
                resume_text,
                job["description"]
            )

            results.append({
                "job_id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "similarity_score": score,
                **gap,
                "recommendations": recommendations,
            })

        results.sort(
            key=lambda item: item["similarity_score"],
            reverse=True
        )

        with SessionLocal() as session:
            record = Analysis(
                filename=Path(file.filename).name,
                results=results
            )

            session.add(record)
            session.commit()
            session.refresh(record)
            analysis_id = record.id

        return {
            "analysis_id": analysis_id,
            "results": results
        }

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
        await file.close()


@app.get("/api/history")
def get_history():
    with SessionLocal() as session:
        records = session.scalars(
            select(Analysis)
            .order_by(Analysis.id.desc())
            .limit(20)
        ).all()

        return [
            {
                "id": record.id,
                "filename": record.filename,
                "created_at": record.created_at.isoformat(),
                "results": record.results,
            }
            for record in records
        ]
