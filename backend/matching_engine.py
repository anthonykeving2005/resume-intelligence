
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def calculate_similarity(
    resume_text: str,
    job_description: str
) -> float:
    embeddings = model.encode(
        [resume_text, job_description],
        normalize_embeddings=True
    )

    score = cosine_similarity(
        embeddings[0:1],
        embeddings[1:2]
    )[0][0]

    return round(float(score) * 100, 2)
