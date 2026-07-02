from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ------------------------------------
# Load Model (Loads only once)
# ------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ------------------------------------
# Generate Embedding
# ------------------------------------

def generate_embedding(text: str):

    """
    Convert text into a semantic vector.
    """

    if not text.strip():
        text = " "

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


# ------------------------------------
# Similarity Score
# ------------------------------------

def semantic_similarity(job_text, resume_text):

    """
    Returns similarity between 0 and 100.
    """

    job_embedding = generate_embedding(job_text)

    resume_embedding = generate_embedding(resume_text)

    similarity = cosine_similarity(
        [job_embedding],
        [resume_embedding]
    )[0][0]

    similarity = max(similarity,0)

    return round(similarity*100,2)


# ------------------------------------
# Batch Embeddings
# ------------------------------------

def batch_embeddings(text_list):

    return model.encode(
        text_list,
        convert_to_numpy=True,
        normalize_embeddings=True
    )