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