def calculate_ats_score(
    resume_text,
    resume_data,
    matched_skills,
    jd_skills
):
    # ---------------------------------------
    # 1. Skill Match Score - 50%
    # ---------------------------------------

    if jd_skills:
        skill_score = (
            len(matched_skills) / len(jd_skills)
        ) * 100
    else:
        skill_score = 0


    # ---------------------------------------
    # 2. Resume Sections - 20%
    # ---------------------------------------

    text = resume_text.lower()

    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    sections_found = sum(
        1 for section in sections
        if section in text
    )

    section_score = (
        sections_found / len(sections)
    ) * 100


    # ---------------------------------------
    # 3. Keyword Match - 20%
    # ---------------------------------------

    if jd_skills:
        keyword_score = (
            len(matched_skills) / len(jd_skills)
        ) * 100
    else:
        keyword_score = 0


    # ---------------------------------------
    # 4. Contact Information - 10%
    # ---------------------------------------

    contact_fields = [
        resume_data.get("email"),
        resume_data.get("phone"),
        resume_data.get("linkedin")
    ]

    contact_found = sum(
        1 for field in contact_fields
        if field
    )

    contact_score = (
        contact_found / len(contact_fields)
    ) * 100


    # ---------------------------------------
    # Final ATS Score
    # ---------------------------------------

    ats_score = (
        skill_score * 0.50
        + section_score * 0.20
        + keyword_score * 0.20
        + contact_score * 0.10
    )

    return round(ats_score)
