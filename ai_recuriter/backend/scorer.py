from backend.embeddings import semantic_similarity
from backend.parser import candidate_to_text

def calculate_skill_score(job_text, candidate):

    """
    Calculates how many candidate skills
    appear in the job description.
    """

    job_text = job_text.lower()

    candidate_skills = [

        skill["name"].lower()

        for skill in candidate["skills"]

    ]

    matched = 0

    for skill in candidate_skills:

        if skill in job_text:

            matched += 1

    if len(candidate_skills) == 0:
        return 0

    return round(
        (matched / len(candidate_skills)) * 100,
        2
    )

def calculate_experience_score(candidate):

    years = candidate["profile"]["years_of_experience"]

    if years >= 8:
        return 100

    elif years >= 6:
        return 90

    elif years >= 5:
        return 80

    elif years >= 3:
        return 60

    return 30

# -----------------------------------------
# Product Company Score
# -----------------------------------------

SERVICE_COMPANIES = {

    "tcs",
    "infosys",
    "wipro",
    "accenture",
    "cognizant",
    "capgemini",
    "hcl",
    "tech mahindra"

}
CAREER_KEYWORDS = {
    "ranking",
    "recommendation",
    "recommendation system",
    "retrieval",
    "search",
    "semantic search",
    "embedding",
    "embeddings",
    "vector",
    "vector database",
    "faiss",
    "pinecone",
    "weaviate",
    "milvus",
    "qdrant",
    "llm",
    "rag",
    "machine learning",
    "deep learning",
    "production",
    "deployment",
    "evaluation",
    "relevance"
}

def calculate_product_score(candidate):

    history = candidate["career_history"]

    product_years = 0

    for job in history:

        company = job["company"].lower()

        is_service = any(
            service_company in company
            for service_company in SERVICE_COMPANIES
        )

        if not is_service:
            product_years += job["duration_months"]

    years = product_years / 12

    if years >= 4:
        return 100

    elif years >= 2:
        return 80

    elif years >= 1:
        return 60

    return 30

# -----------------------------------------
# Career History Score
# -----------------------------------------

def calculate_career_score(candidate):

    history = candidate["career_history"]

    score = 0

    for job in history:

        description = job["description"].lower()

        for keyword in CAREER_KEYWORDS:

            if keyword in description:

                score += 5

    return min(score, 100)
# -----------------------------------------
# Redrob Platform Score
# -----------------------------------------

def calculate_signal_score(candidate):

    signals = candidate["redrob_signals"]

    score = 0

    # -------------------------
    # Open to Work
    # -------------------------
    if signals["open_to_work_flag"]:
        score += 15

    # -------------------------
    # Verified Profile
    # -------------------------
    if signals["verified_email"]:
        score += 5

    if signals["verified_phone"]:
        score += 5

    if signals["linkedin_connected"]:
        score += 5

    # -------------------------
    # Profile Completeness
    # -------------------------
    score += min(
        signals["profile_completeness_score"] * 0.25,
        25
    )

    # -------------------------
    # Recruiter Response Rate
    # -------------------------
    score += signals["recruiter_response_rate"] * 10

    # -------------------------
    # Interview Completion
    # -------------------------
    score += signals["interview_completion_rate"] * 10

    # -------------------------
    # GitHub Activity
    # -------------------------
    github = signals["github_activity_score"]

    if github > 0:
        score += min(github / 5, 10)

    # -------------------------
    # Saved by Recruiters
    # -------------------------
    score += min(
        signals["saved_by_recruiters_30d"],
        10
    )

    return round(min(score, 100), 2)

# -----------------------------------------
# Final Candidate Score
# -----------------------------------------

def final_score(job_text, candidate):
    """
    Calculates the final weighted score for a candidate.
    """

    candidate_text = candidate_to_text(candidate)

    semantic = semantic_similarity(
        job_text,
        candidate_text
    )

    skill = calculate_skill_score(
        job_text,
        candidate
    )

    experience = calculate_experience_score(
        candidate
    )

    product = calculate_product_score(
        candidate
    )

    signals = calculate_signal_score(
        candidate
    )
    career = calculate_career_score(
    candidate
)

    final = (

    semantic * 0.35 +

    skill * 0.20 +

    experience * 0.10 +

    product * 0.10 +

    signals * 0.10 +

    career * 0.15

)

    return {

        "semantic_score": round(semantic, 2),

        "skill_score": round(skill, 2),

        "experience_score": round(experience, 2),

        "product_score": round(product, 2),

        "signal_score": round(signals, 2),
        "career_score": round(career, 2),

        "final_score": round(final, 2)

    }
def candidate_assessment(job_text, candidate, scores):
    strengths = []
    weaknesses = []
    recommendation = ""
    semantic = scores["semantic_score"]
    skill = scores["skill_score"]
    experience = scores["experience_score"]
    product = scores["product_score"]
    signal = scores["signal_score"]
    final = scores["final_score"]
    # -----------------------------------------
# Strengths
# -----------------------------------------

    if semantic >= 70:
        strengths.append(
        "Excellent semantic match with the Job Description."
    )

    elif semantic >= 50:
        strengths.append(
        "Good semantic similarity with the Job Description."
    )

    if skill >= 70:
        strengths.append(
        "Strong technical skill match."
    )

    elif skill >= 50:
        strengths.append(
        "Good technical skill coverage."
    )

    if experience >= 80:
        strengths.append(
        "Strong industry experience."
    )

    if product >= 80:
        strengths.append(
        "Relevant product company experience."
    )

    if signal >= 70:
        strengths.append(
        "Highly verified and complete candidate profile."
    )
        
    # -----------------------------------------
# Needs Improvement
# -----------------------------------------

    if semantic < 50:
        weaknesses.append(
        "Profile has limited similarity with the Job Description."
        )

    if skill < 50:
        weaknesses.append(
        "Candidate is missing some required technical skills."
        )

    if experience < 80:
        weaknesses.append(
        "Could benefit from more relevant industry experience."
        )

    if product < 80:
        weaknesses.append(
        "Limited product company experience."
        )

    if signal < 70:
        weaknesses.append(
        "Profile completeness and verification can be improved."
        )  

    # -----------------------------------------
# Hiring Recommendation
# -----------------------------------------

    if final >= 55:
        recommendation = "✅ Recommended for Interview"

    elif final >= 45:
        recommendation = "🟡 Proceed with Technical Assessment"

    else:
        recommendation = "❌ Not Recommended Currently"  
    return {
    "strengths": strengths,
    "weaknesses": weaknesses,
    "recommendation": recommendation
}
def recruiter_category(candidate):
    if candidate["rank"] == 1:
        return "🟢 Ready for Interview"

    elif candidate["rank"] <= 3:
        return "🟡 Technical Assessment"

    elif candidate["rank"] <= 5:
        return "🔵 Talent Pool"

    else:
        return "🔴 Not Recommended"
    