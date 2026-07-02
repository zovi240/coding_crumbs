import os
import pandas as pd


# ----------------------------------------
# Create Folder
# ----------------------------------------

def create_folder(folder_path):

    os.makedirs(folder_path, exist_ok=True)


# ----------------------------------------
# Save Uploaded File
# ----------------------------------------

def save_uploaded_file(uploaded_file, folder="uploads"):

    create_folder(folder)

    file_path = os.path.join(folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# ----------------------------------------
# Save Ranking CSV
# ----------------------------------------

def save_results(results, filename="outputs/candidate_rankings.csv"):

    create_folder("outputs")

    df = pd.DataFrame(results)

    df.to_csv(filename, index=False)

    return filename


# ----------------------------------------
# Load CSV
# ----------------------------------------

def load_results(filename):

    return pd.read_csv(filename)


# ----------------------------------------
# Convert Score to Percentage
# ----------------------------------------

def percentage(score):

    return f"{round(score,2)}%"


# ----------------------------------------
# Get Top Candidate
# ----------------------------------------

def best_candidate(results):

    if len(results) == 0:
        return None

    return max(results, key=lambda x: x["final_score"])


# ----------------------------------------
# Statistics
# ----------------------------------------

def statistics(results):

    if len(results) == 0:

        return {

            "total_candidates": 0,
            "highest_score": 0,
            "average_score": 0

        }

    scores = [candidate["final_score"] for candidate in results]

    return {

        "total_candidates": len(scores),

        "highest_score": max(scores),

        "average_score": round(sum(scores) / len(scores), 2)

    }

def save_submission(results, filename="outputs/submission.csv"):

    create_folder("outputs")

    submission = []

    for candidate in results[:100]:

        reason = []

        if candidate["semantic_score"] >= 70:
            reason.append("Strong semantic match")

        if candidate["skill_score"] >= 70:
            reason.append("Good technical skill match")

        if candidate["experience"] >= 5:
            reason.append("Relevant industry experience")

        if candidate["career_score"] >= 50:
            reason.append("Relevant AI project experience")

        if candidate["signal_score"] >= 70:
            reason.append("Strong recruiter profile")

        if len(reason) == 0:
            reason.append("Candidate requires further evaluation")

        submission.append({
            "candidate_id": candidate["candidate_id"],
            "rank": candidate["rank"],
            "score": candidate["final_score"],
            "reasoning": "; ".join(reason)
        })

    pd.DataFrame(submission).to_csv(filename, index=False)

    return filename

