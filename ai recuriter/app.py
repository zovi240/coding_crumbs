import streamlit as st
import pandas as pd

from backend.parser import (
    read_job_description,
    load_candidates
)

from backend.scorer import (
    final_score,
    candidate_assessment
)
from backend.ranking import rank_candidates
from backend.utils import save_results

from backend.dashboard import (
    score_chart,
    skills_chart,
    recommendation_chart,
    distribution_chart
)
from recruitment import recruitment_center

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Candidate Ranking System",
    page_icon="🤖",
    layout="wide"
)
page = st.sidebar.radio(
    "📂 Navigation",
    [
        "🏠 Candidate Ranking",
        "📧 Recruitment Center"
    ]
)

if page == "📧 Recruitment Center":
    recruitment_center()
    st.stop()
# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main{
    padding-top:20px;
}

.block-container{
    padding-top:2rem;
}

div.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🤖 AI Candidate Ranking System")

st.caption(
    "AI Powered Candidate Ranking using Semantic Search"
)

st.divider()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("Instructions")

    st.write("""
1. Upload Job Description (.docx)

2. Upload candidates.jsonl

3. Click Rank Candidates

4. Download Results
""")

    st.success("System Ready")

# ---------------------------------------------------
# FILE UPLOADS
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    job_file = st.file_uploader(
        "📄 Job Description",
        type=["docx"]
    )

with right:

    candidates_file = st.file_uploader(
        "👥 Candidates Dataset",
        type=["jsonl","json"]
    )

st.divider()

# ---------------------------------------------------
# START BUTTON
# ---------------------------------------------------

rank_button = st.button(
    "🚀 Rank Candidates"
)
# ---------------------------------------------------
# PROCESS CANDIDATES
# ---------------------------------------------------

if rank_button:

    # -------------------------
    # Validation
    # -------------------------

    if job_file is None:

        st.error("Please upload the Job Description.")

        st.stop()

    if candidates_file is None:

        st.error("Please upload candidates.jsonl. or candidate.jsonl.")

        st.stop()

    # -------------------------
    # Progress
    # -------------------------

    progress = st.progress(0)

    status = st.empty()

    # -------------------------
    # Read Job Description
    # -------------------------

    status.info("Reading Job Description...")

    job_text = read_job_description(job_file)

    progress.progress(20)

    # -------------------------
    # Load Candidates
    # -------------------------

    status.info("Loading Candidates...")

    candidates = load_candidates(candidates_file)

    progress.progress(40)

    results = []

    total = len(candidates)

    # -------------------------
    # Score Candidates
    # -------------------------

    for index, candidate in enumerate(candidates):

        status.info(
            f"Scoring candidate {index+1} of {total}"
        )

        score = final_score(
            job_text,
            candidate
        )
        assessment = candidate_assessment(
        job_text,
        candidate,
        score
        )

        candidate_result = {

            "candidate_id": candidate["candidate_id"],

            "Candidate": candidate["profile"]["anonymized_name"],

            "headline": candidate["profile"]["headline"],
            

            "experience": candidate["profile"]["years_of_experience"],
            "skills": candidate["skills"],
            "education": candidate["education"],
            "career_history": candidate["career_history"],
            "redrob_signals": candidate["redrob_signals"],

            "semantic_score": score["semantic_score"],

            "skill_score": score["skill_score"],

            "experience_score": score["experience_score"],

            "product_score": score["product_score"],

            "signal_score": score["signal_score"],
            "career_score": score["career_score"],

            "final_score": score["final_score"],
            "strengths": assessment["strengths"],

            "weaknesses": assessment["weaknesses"],

            "recommendation": assessment["recommendation"]

        }

        results.append(candidate_result)

        progress.progress(
            40 + int((index + 1) / total * 50)
        )

    # -------------------------
    # Ranking
    # -------------------------

    ranked = rank_candidates(results)
    st.session_state["ranked"] = ranked

    progress.progress(100)

    status.success("Ranking Complete!")
if "ranked" in st.session_state:

    ranked = st.session_state["ranked"]

    df = pd.DataFrame(ranked)
        # ---------------------------------------------------
        # RESULTS
        # ---------------------------------------------------
    st.divider()

    st.header("🏆 Candidate Rankings")

    df = pd.DataFrame(ranked)

    display_df = df[
        [
            "rank",
            "Candidate",
            "headline",
            "experience",
            "final_score"
        ]
    ]

    st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
                "Total Candidates",
                len(df)
            )

    with col2:
        st.metric(
                "Highest Score",
                f"{df['final_score'].max():.2f}"
            )

    with col3:
        st.metric(
                "Average Score",
                f"{df['final_score'].mean():.2f}"
            )

    st.divider()

    st.header("📈 Analytics")

    chart1 = score_chart(ranked)

    st.plotly_chart(
            chart1,
            use_container_width=True
        )

    chart2 = distribution_chart(ranked)

    st.plotly_chart(
            chart2,
            use_container_width=True
        )

    st.divider()

    csv_file = save_results(ranked)

    with open(csv_file, "rb") as file:

        st.download_button(
                "📥 Download Rankings",
                file,
                file_name="candidate_rankings.csv",
                mime="text/csv"
            )

    st.success("🎉 Ranking Completed Successfully!")

    st.divider()

    st.header("👤 Candidate Details")

    selected_candidate = st.selectbox(
            "Select a Candidate",
            df["Candidate"]
        )

    candidate_info = next(
            candidate
            for candidate in ranked
            if candidate["Candidate"] == selected_candidate
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
                "🏆 Final Score",
                f"{candidate_info['final_score']:.2f}"
            )
        rank = candidate_info["rank"]
        score = candidate_info["final_score"]

        if rank == 1 and score >= 55:
            recommendation = "🟢 Excellent Match"

        elif score >= 50:
            recommendation = "🟢 Strong Match"

        elif score >= 45:
            recommendation = "🟡 Good Match"

        elif score >= 35:
            recommendation = "🟠 Average Match"

        else:
            recommendation = "🔴 Weak Match"

        st.success(recommendation)

        st.metric(
                "💼 Experience",
                candidate_info["experience"]
            )

        st.write("### 📊 Score Breakdown")

        semantic = float(candidate_info["semantic_score"])
        skill = float(candidate_info["skill_score"])
        career = float(candidate_info["career_score"])
        product = float(candidate_info["product_score"])
        signal = float(candidate_info["signal_score"])

        st.progress(semantic / 100)
        st.caption(f"Semantic Match : {semantic:.2f}")

        st.progress(skill / 100)
        st.caption(f"Skill Match : {skill:.2f}")

        st.progress(career / 100)
        st.caption(f"Career Score : {career:.2f}")

        st.progress(product / 100)
        st.caption(f"Product Score : {product:.2f}")

        st.progress(signal / 100)
        st.caption(f"Signal Score : {signal:.2f}")

        st.divider()

        st.header("🤖 AI Candidate Assessment")

        st.write("### ✅ Strengths")

        for strength in candidate_info["strengths"]:
            st.write(f"• {strength}")

        st.write("### ⚠ Needs Improvement")

        for weakness in candidate_info["weaknesses"]:
            st.write(f"• {weakness}")

        st.write("### 📌 Hiring Recommendation")

        recommendation = candidate_info["recommendation"]

        if "Interview" in recommendation:
            st.success(recommendation)

        elif "Technical" in recommendation:
            st.warning(recommendation)

        else:
            st.error(recommendation)

    with col2:

        st.write("### Headline")
        st.write(candidate_info["headline"])

        st.write("### Candidate ID")
        st.write(candidate_info["candidate_id"])

        st.write("### 🛠 Skills")

        skills = [
            skill["name"]
            for skill in candidate_info["skills"]
        ]

        skill_html = ""

        for skill in skills:
            skill_html += (
                f'<span style="'
                'display:inline-block;'
        'background:#E8F1FF;'
        'color:#1E3A8A;'
        'padding:6px 12px;'
        'margin:5px;'
        'border-radius:20px;'
        'font-size:14px;'
        'font-weight:600;'
                '">'
                f'{skill}'
                '</span>'
            )

        st.markdown(skill_html, unsafe_allow_html=True)
        with st.expander("### 🎓 Education"):

            education = [
                f"{edu['degree']} - {edu['field_of_study']}"
                for edu in candidate_info["education"]
            ]

            for edu in education:
                st.write("•", edu)
        with st.expander("### 💼 Career History"):

            for job in candidate_info["career_history"]:

                st.write(f"**{job['title']}**")

                st.write(job["company"])

                st.write(f"{job['duration_months']} months")

                st.write(job["description"])

                st.divider()

        with st.expander("### 📈 Redrob Signals"):

            signals = candidate_info["redrob_signals"]

            st.write(
                "✅ Open to Work"
                if signals["open_to_work_flag"]
                else "❌ Open to Work"
            )

            st.write(
                "✅ Verified Email"
                if signals["verified_email"]
                else "❌ Verified Email"
            )

            st.write(
                "✅ Verified Phone"
                if signals["verified_phone"]
                else "❌ Verified Phone"
            )

            st.write(
                "✅ LinkedIn Connected"
                if signals["linkedin_connected"]
                else "❌ LinkedIn Connected"
            )

            st.write(
                f"Profile Completeness: {signals['profile_completeness_score']}%"
            )

            st.write(
                f"GitHub Activity: {signals['github_activity_score']}"
            )

            st.write(
                f"Recruiter Response Rate: {signals['recruiter_response_rate']}"
            )

            st.write(
                f"Interview Completion Rate: {signals['interview_completion_rate']}"
            )