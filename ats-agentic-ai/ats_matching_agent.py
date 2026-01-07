def calculate_ats_score(resume_text, job_skills):
    matched = [skill for skill in job_skills if skill in resume_text]
    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0
    return round(score, 2), matched
