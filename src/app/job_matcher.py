def match_resume_to_jobs(resume_text, job_listings):
    matches = []

    resume_keywords = set(resume_text.lower().split())

    for job in job_listings:
        job_keywords = set(job["description"].lower().split())
        score = len(resume_keywords & job_keywords)
        job["match_score"] = score
        matches.append(job)

    return sorted(matches, key=lambda x: x["match_score"], reverse=True)