
import re

SKILLS = {
    "python": ["python"],
    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "sql": ["sql"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "nlp": ["natural language processing", "nlp"],
    "react": ["react.js", "react"],
    "fastapi": ["fastapi"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "git": ["git", "github"],
    "java": ["java"],
    "flask": ["flask"],
    "mongodb": ["mongodb"],
    "mysql": ["mysql"],
    "rest api": ["rest api", "restful api"],
}


def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found = []

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

            if re.search(pattern, text):
                found.append(skill)
                break

    return sorted(found)


def analyze_skill_gap(resume_text: str, job_description: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    required_skills = set(extract_skills(job_description))

    return {
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required_skills),
        "matched_skills": sorted(resume_skills & required_skills),
        "missing_skills": sorted(required_skills - resume_skills),
    }
