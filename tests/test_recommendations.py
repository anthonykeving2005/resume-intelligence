
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "backend")
)

from recommendations import recommend_skills


def test_known_skill_recommendation():
    result = recommend_skills(["fastapi"])

    assert len(result) == 1
    assert result[0]["skill"] == "fastapi"
    assert result[0]["priority"] == "High"


def test_unknown_skill_has_fallback():
    result = recommend_skills(["some-new-skill"])

    assert len(result) == 1
    assert "action" in result[0]
    assert "project" in result[0]
