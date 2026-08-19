def analyze_sections(resume_text):

    text = resume_text.lower()

    sections = {
        "Summary": [
            "summary",
            "profile",
            "objective"
        ],

        "Skills": [
            "skills",
            "technical skills"
        ],

        "Education": [
            "education",
            "academic"
        ],

        "Experience": [
            "experience",
            "work experience",
            "internship"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certifications",
            "certification",
            "courses"
        ]
    }

    result = {}

    for section, keywords in sections.items():

        found = any(
            keyword in text
            for keyword in keywords
        )

        result[section] = found

    return result