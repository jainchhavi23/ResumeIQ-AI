import re


def extract_email(text):
    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
        text
    )

    return match.group(0) if match else None


def extract_linkedin(text):
    match = re.search(
        r'https?://(?:www\.)?linkedin\.com/[^\s|]+',
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else None


def extract_github(text):
    match = re.search(
        r'https?://(?:www\.)?github\.com/[^\s|]+',
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else None


def extract_name(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    for line in lines[:5]:

        if (
            len(line.split()) <= 4
            and not re.search(r'[@:/|0-9]', line)
            and line.lower() not in [
                "resume",
                "curriculum vitae",
                "cv"
            ]
        ):
            return line.title()

    return None


def parse_resume(text):
    """
    Extract basic information from resume text.
    """

    resume_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text)
    }

    return resume_data