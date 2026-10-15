
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "backend")
)

from skills import analyze_skill_gap, extract_skills


def test_extract_skills():
    skills = extract_skills(
        "Experienced in Python, machine learning and SQL."
    )

    assert "python" in skills
    assert "machine learning" in skills
    assert "sql" in skills


def test_skill_gap():
    result = analyze_skill_gap(
        "I use Python and SQL.",
        "Python, SQL and Docker are required."
    )

    assert "python" in result["matched_skills"]
    assert "sql" in result["matched_skills"]
    assert "docker" in result["missing_skills"]
