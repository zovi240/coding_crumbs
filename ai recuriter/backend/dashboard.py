import plotly.express as px
import pandas as pd


# ----------------------------------------
# Candidate Score Chart
# ----------------------------------------

def score_chart(results):

    df = pd.DataFrame(results)

    fig = px.bar(
        df,
        x="Candidate",
        y="final_score",
        color="final_score",
        title="Candidate Ranking",
        text="final_score"
    )

    fig.update_layout(
        xaxis_title="Candidate",
        yaxis_title="Score",
        height=450
    )

    return fig


# ----------------------------------------
# Skills Distribution
# ----------------------------------------

def skills_chart(results):

    skills = []

    for candidate in results:

        if "skills" in candidate:

            skills.extend(candidate["skills"])

    if len(skills) == 0:

        return None

    df = pd.DataFrame(skills, columns=["Skill"])

    counts = df["Skill"].value_counts().reset_index()

    counts.columns = ["Skill", "Count"]

    fig = px.pie(
        counts,
        names="Skill",
        values="Count",
        title="Top Skills"
    )

    return fig


# ----------------------------------------
# Recommendation Chart
# ----------------------------------------

def recommendation_chart(results):

    recommendations = []

    for candidate in results:

        recommendations.append(
            candidate["recommendation"]
        )

    df = pd.DataFrame(
        recommendations,
        columns=["Recommendation"]
    )

    counts = (
        df["Recommendation"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Recommendation",
        "Count"
    ]

    fig = px.bar(
        counts,
        x="Recommendation",
        y="Count",
        color="Recommendation",
        title="AI Recommendations"
    )

    return fig


# ----------------------------------------
# Score Distribution
# ----------------------------------------

def distribution_chart(results):

    df = pd.DataFrame(results)

    fig = px.histogram(
        df,
        x="final_score",
        nbins=10,
        title="Score Distribution"
    )

    return fig