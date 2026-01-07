import streamlit as st

from resume_agent import parse_resume
from job_agent import get_job_skills, ITI_JOBS
from ats_agent import calculate_ats_score
from decision_agent import make_decision
from feedback_agent import generate_feedback

st.set_page_config(page_title="ITI ATS Resume Checker", layout="centered")

st.title("🔧 ITI ATS Resume Checker")
st.subheader("Check job match for ITI trades")

job_role = st.selectbox("Select ITI Job Role", ITI_JOBS.keys())
resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if st.button("Check ATS Score"):
    if resume_file:
        resume_text = parse_resume(resume_file)
        job_skills = get_job_skills(job_role)

        score, matched = calculate_ats_score(resume_text, job_skills)
        decision = make_decision(score)
        missing, feedback = generate_feedback(job_skills, matched)

        st.metric("ATS Score", f"{score}%")
        st.write("### Decision:", decision)
        st.write("### Matched Skills:", matched)
        st.write("### Missing Skills:", missing)
        st.info(feedback)
    else:
        st.warning("Please upload a resume PDF")
