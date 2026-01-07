import gradio as gr
import pdfplumber
import spacy
from sklearn.metrics import jaccard_score
import numpy as np

# Load spaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ITI Job Skill Database
ITI_JOBS = {
    "Fitter": ["fitting", "maintenance", "mechanical", "tools", "assembly"],
    "Welder": ["welding", "fabrication", "metal", "arc welding", "gas welding"],
    "Electrician": ["wiring", "electrical", "circuit", "maintenance", "repair"],
    "Plumber": ["plumbing", "pipes", "fitting", "water supply", "maintenance"],
    "Machinist": ["lathe", "machine", "cutting", "drilling", "manufacturing"],
    "Turner": ["turning", "lathe", "machine"],
    "Diesel Mechanic": ["diesel engine", "repair", "maintenance", "mechanic"]
}

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def preprocess(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

def calculate_ats_score(resume_text, job_skills):
    resume_tokens = preprocess(resume_text)
    job_tokens = job_skills

    all_tokens = list(set(resume_tokens + job_tokens))
    resume_vector = [1 if t in resume_tokens else 0 for t in all_tokens]
    job_vector = [1 if t in job_tokens else 0 for t in all_tokens]

    score = jaccard_score(resume_vector, job_vector)
    return round(score * 100, 2)

def ats_matcher(pdf_file, job_role):
    resume_text = extract_text_from_pdf(pdf_file)
    job_skills = ITI_JOBS[job_role]

    score = calculate_ats_score(resume_text, job_skills)

    decision = (
        "✅ MATCHED" if score >= 40 else
        "⚠️ NEEDS IMPROVEMENT" if score >= 25 else
        "❌ NOT MATCHED"
    )

    return {
        "ats_score": score,
        "decision": decision,
        "matched_skills": [s for s in job_skills if s in resume_text],
        "missing_skills": [s for s in job_skills if s not in resume_text],
        "feedback": "Improve missing skills for better job match."
    }

def ui_handler(pdf, job):
    result = ats_matcher(pdf, job)
    return f"""
ATS Score: {result['ats_score']} %

Decision: {result['decision']}

Matched Skills:
{', '.join(result['matched_skills'])}

Missing Skills:
{', '.join(result['missing_skills'])}

Feedback:
{result['feedback']}
"""

gr.Interface(
    fn=ui_handler,
    inputs=[
        gr.File(label="Upload Resume (PDF)"),
        gr.Dropdown(list(ITI_JOBS.keys()), label="Select ITI Job Role")
    ],
    outputs=gr.Textbox(label="ATS Evaluation Result"),
    title="ITI ATS Agentic AI",
    description="ATS Resume Matching System for ITI Students (Fitter, Welder, Electrician, Plumber, etc.)"
).launch()
