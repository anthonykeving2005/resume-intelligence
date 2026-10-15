
import fitz


def extract_resume_text(file_path: str) -> str:
    """Extract text from a text-based PDF resume."""
    pages = []

    with fitz.open(file_path) as pdf:
        for page in pdf:
            pages.append(page.get_text())

    return "\n".join(pages).strip()
