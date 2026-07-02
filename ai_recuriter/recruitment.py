import streamlit as st

def recruitment_center():

    # ---------------------------------------
    # Check if candidates have been ranked
    # ---------------------------------------

    if "ranked" not in st.session_state:
        st.warning("⚠ Please rank candidates first.")
        return

    ranked = st.session_state["ranked"]

    # ---------------------------------------
    # Categorize Candidates
    # ---------------------------------------

    interview = []
    technical = []
    rejected = []

    for candidate in ranked:

        rank = candidate["rank"]

        if rank <= 5:
            interview.append(candidate)

        elif rank <= 15:
            technical.append(candidate)

        else:
            rejected.append(candidate)

    # ---------------------------------------
    # UI Starts Here
    # ---------------------------------------

    st.title("📧 Recruitment Center")

    st.subheader("📊 Recruitment Summary")

    col1, col2, col3 = st.columns(3)

    st.metric(
    "🟢 Ready for Interview",
    len(interview)
    )

    st.metric(
    "🟡 Technical Assessment",
    len(technical)
    )

    st.metric(
    "🔴 Not Recommended",
    len(rejected)
    )

    st.divider()

    st.subheader("🟢 Ready for Interview")

    import pandas as pd

    interview_df = pd.DataFrame(interview)

    if not interview_df.empty:

        st.dataframe(
            interview_df[
                [
                "rank",
                "Candidate",
                "headline",
                "experience",
                "final_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No candidates available.")

    if st.button("✨ Generate Interview Invitation"):
        st.session_state["show_interview_template"] = True
    if st.session_state.get("show_interview_template", False):

        st.subheader("📧 Interview Invitation")

        subject = st.text_input(
        "Subject",
            value="Interview Invitation – Senior AI Engineer"
        )

        body = st.text_area(
        "Email Body",
            value="""Dear {Candidate Name},

    Congratulations!

    After reviewing your application, we are pleased to invite you to the next stage of our recruitment process.

    Our recruitment team will contact you shortly with the interview schedule.

    Best Regards,
    HR Team""",
            height=250
        )
        st.subheader("👥 Recipients")
        selected_candidates = []

        for candidate in interview:

            if st.checkbox(
                candidate["Candidate"],
                value=True,
                key=f"interview_{candidate['candidate_id']}"
            ):
                selected_candidates.append(candidate)
        if st.button(
            "📧 Send Invitations",
            key="send_interview"
        ):
            st.success("✅ Interview invitations sent successfully!")

    st.divider()

    st.subheader("🟡 Technical Assessment")

    technical_df = pd.DataFrame(technical)

    if not technical_df.empty:

        st.dataframe(
            technical_df[
                [
                "rank",
                "Candidate",
                "headline",
                "experience",
                "final_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No candidates available.")

    if st.button("✨ Generate technical assesment Invitation"):
        st.session_state["show_technical_template"] = True
    if st.session_state.get("show_technical_template", False):

        st.subheader("📧 technical Invitation")

        subject = st.text_input(
        "Subject",
            value="Technical Assessment Invitation – Senior AI Engineer"
        )

        body = st.text_area(
        "Email Body",
            value="""Dear {Candidate Name},

    Thank you for your interest in the Senior AI Engineer position.

    After reviewing your application, we would like to invite you to complete a technical assessment as the next step in our recruitment process.

    The assessment will help us better understand your technical skills and problem-solving abilities.

    Our recruitment team will share the assessment details shortly.
    Best Regards,
    HR Team""",
            height=250
        )
        st.subheader("👥 Recipients")
        selected_candidates = []

        for candidate in technical:

            if st.checkbox(
                candidate["Candidate"],
                value=True,
                key=f"technical_{candidate['candidate_id']}"
            ):
                selected_candidates.append(candidate)
        if st.button(
            "📝 Send Assessment Invitations",
            key="send_technical"
        ):
            st.success("✅ Technical Assessment Invitations sent successfully!")

    st.divider()

    st.subheader("🔴 Not Recommended")

    rejected_df = pd.DataFrame(rejected)

    if not rejected_df.empty:

        st.dataframe(
            rejected_df[
                [
                "rank",
                "Candidate",
                "headline",
                "experience",
                "final_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No candidates available.")

    if st.button("✨ Generate Application Update"):
        st.session_state["show_rejected_template"] = True
    if st.session_state.get("show_rejected_template", False):

        st.subheader("📧 Application Update")

        subject = st.text_input(
        "Subject",
            value="Application Update – Senior AI Engineer"
        )

        body = st.text_area(
        "Email Body",
            value="""Dear {Candidate Name},

    Thank you for taking the time to apply for the Senior AI Engineer position.

    After carefully reviewing your application, we have decided not to move forward with your application for this role.

    We sincerely appreciate your interest in our company and encourage you to apply again for future opportunities that match your skills and experience.

    We wish you all the best in your future endeavors.

    Best Regards,
    HR Team""",
            height=250
        )
        st.subheader("👥 Recipients")
        selected_candidates = []

        for candidate in rejected:

            if st.checkbox(
                candidate["Candidate"],
                value=True,
                key=f"rejected_{candidate['candidate_id']}"
            ):
                selected_candidates.append(candidate)
        if st.button(
            "📄 Send Application Updates",
            key="send_rejected"
        ):
            st.success("✅ Application Update emails sent successfully!")