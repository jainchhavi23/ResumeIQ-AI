from services.skills_extractor import SKILLS_DATABASE, extract_skills


def extract_jd_skills(job_description):
    """
    Extract required skills from a job description.
    """

    if not job_description:
        return []

    return extract_skills(job_description)