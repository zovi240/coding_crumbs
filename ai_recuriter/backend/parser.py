import json
from docx import Document


# -----------------------------
# Read Job Description (.docx)
# -----------------------------
def read_job_description(uploaded_file):
    """
    Reads a DOCX job description and returns plain text.
    """

    document = Document(uploaded_file)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    return text


# -----------------------------
# Read Candidates (.json / .jsonl)
# -----------------------------
def load_candidates(uploaded_file):
    """
    Reads candidates from JSON or JSONL.
    """

    uploaded_file.seek(0)

    filename = uploaded_file.name.lower()

    # -----------------------------
    # JSON
    # -----------------------------
    if filename.endswith(".json"):

        candidates = json.load(uploaded_file)

        uploaded_file.seek(0)

        return candidates

    # -----------------------------
    # JSONL
    # -----------------------------
    elif filename.endswith(".jsonl"):

        candidates = []

        for line in uploaded_file:

            if line.strip():

                candidates.append(
                    json.loads(line)
                )

        uploaded_file.seek(0)

        return candidates

    else:

        raise ValueError("Unsupported file format.")
# -----------------------------
# Convert Candidate to Text
# -----------------------------
def candidate_to_text(candidate):
    """
    Converts a structured candidate profile into
    one text block for semantic embeddings.
    """

    profile = candidate["profile"]

    skills = ", ".join(
        skill["name"]
        for skill in candidate["skills"]
    )

    experience = "\n".join(

        f"{job['title']} at {job['company']}. {job['description']}"

        for job in candidate["career_history"]

    )

    education = "\n".join(

        f"{edu['degree']} in {edu['field_of_study']}"

        for edu in candidate["education"]

    )

    text = f"""
Headline:
{profile['headline']}

Summary:
{profile['summary']}

Skills:
{skills}

Experience:
{experience}

Education:
{education}
"""

    return text