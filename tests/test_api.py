
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "backend")
)

import main
from database import Base


@pytest.fixture
def client(monkeypatch):
    # Use a separate temporary database for testing.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSession = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)
    monkeypatch.setattr(main, "SessionLocal", TestingSession)

    with TestClient(main.app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Resume Intelligence API"


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_jobs_endpoint(client):
    response = client.get("/api/jobs")

    assert response.status_code == 200

    jobs = response.json()
    assert isinstance(jobs, list)
    assert len(jobs) > 0
    assert "title" in jobs[0]
    assert "description" in jobs[0]


def test_reject_non_pdf_upload(client):
    response = client.post(
        "/api/analyze",
        files={
            "file": (
                "resume.txt",
                b"This is not a PDF",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_analyze_resume_and_save_history(client, monkeypatch):
    # Mock PDF extraction and the AI similarity model.
    # This makes the test fast and avoids model inference.
    monkeypatch.setattr(
        main,
        "extract_resume_text",
        lambda file_path: "Python machine learning SQL",
    )
    monkeypatch.setattr(
        main,
        "calculate_similarity",
        lambda resume, description: 80.0,
    )

    response = client.post(
        "/api/analyze",
        files={
            "file": (
                "sample_resume.pdf",
                b"%PDF-1.4 fake PDF for mocked test",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "analysis_id" in data
    assert len(data["results"]) > 0

    first_result = data["results"][0]
    assert "similarity_score" in first_result
    assert "matched_skills" in first_result
    assert "missing_skills" in first_result
    assert "recommendations" in first_result

    # Verify that the analysis was saved to the test database.
    history_response = client.get("/api/history")

    assert history_response.status_code == 200

    history = history_response.json()
    assert len(history) == 1
    assert history[0]["filename"] == "sample_resume.pdf"
    assert history[0]["id"] == data["analysis_id"]
