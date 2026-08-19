def generate_suggestions(
    resume_data,
    matched_skills,
    missing_skills,
    resume_text
):
    suggestions = []

    text = resume_text.lower()

    # Missing skills
    if missing_skills:
        skills = ", ".join(
            skill.title() for skill in missing_skills
        )

        suggestions.append(
            f"Consider adding relevant skills from the job description: {skills}"
        )

    # Email
    if not resume_data.get("email"):
        suggestions.append(
            "Add a professional email address to your resume."
        )

    # Phone
    if not resume_data.get("phone"):
        suggestions.append(
            "Add your phone number to your resume."
        )

    # LinkedIn
    if not resume_data.get("linkedin"):
        suggestions.append(
            "Add your LinkedIn profile URL."
        )

    # GitHub
    if not resume_data.get("github"):
        suggestions.append(
            "Consider adding your GitHub profile, especially for technical roles."
        )

    # Resume sections
    if "education" not in text:
        suggestions.append(
            "Add an Education section."
        )

    if "experience" not in text:
        suggestions.append(
            "Add an Experience section if you have relevant experience."
        )

    if "projects" not in text:
        suggestions.append(
            "Add relevant projects to demonstrate your practical skills."
        )

    if "certification" not in text:
        suggestions.append(
            "Consider adding relevant certifications."
        )

    return suggestions