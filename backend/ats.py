import re

# Master Skill List
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "fastapi",
    "mongodb",
    "mysql",
    "docker",
    "git",
    "github",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "data structures",
    "algorithms"
]


def extract_skills(text):
    """
    Extract all matching skills from a text.
    """
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def calculate_ats_score(resume_text, job_description=None):
    """
    If only resume is provided:
        Returns ATS score based on known skills.

    If resume + JD are provided:
        Returns ATS score based on JD matching.
    """

    resume_skills = extract_skills(resume_text)

    # ----------------------------
    # Resume Only
    # ----------------------------
    if job_description is None:

        score = int((len(resume_skills) / len(SKILLS)) * 100)

        return score, resume_skills

    # ----------------------------
    # Resume vs JD
    # ----------------------------
    jd_skills = extract_skills(job_description)

    matched = list(set(resume_skills) & set(jd_skills))

    if len(jd_skills) == 0:
        score = 0
    else:
        score = int((len(matched) / len(jd_skills)) * 100)

    return score, matched


def compare_resume_with_jd(resume_text, job_description):
    """
    Compare Resume against Job Description.
    """

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched = sorted(list(set(resume_skills) & set(jd_skills)))

    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    extra = sorted(list(set(resume_skills) - set(jd_skills)))

    if len(jd_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = int(
            (len(matched) / len(jd_skills)) * 100
        )

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills
    }