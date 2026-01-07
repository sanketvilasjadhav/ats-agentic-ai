def generate_feedback(job_skills, matched):
    missing = list(set(job_skills) - set(matched))

    if missing:
        feedback = "Improve skills in: " + ", ".join(missing)
    else:
        feedback = "Excellent match for this ITI job role."

    return missing, feedback
