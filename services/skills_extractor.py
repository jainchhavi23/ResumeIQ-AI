import re


SKILLS_DATABASE = [
    # Programming
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "sql",

    # Web
    "html",
    "html5",
    "css",
    "css3",
    "flask",
    "django",
    "fastapi",
    "react",
    "node.js",
    "express",

    # Data / AI
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "generative ai",
    "nlp",

    # Database
    "mysql",
    "postgresql",
    "sqlite",
    "mongodb",
    "sqlalchemy",

    # Tools
    "git",
    "github",
    "docker",
    "aws",
    "power bi",
    "excel",

    # Concepts
    "data analysis",
    "data cleaning",
    "exploratory data analysis",
    "eda",
    "rest api",
    "api",
]


def extract_skills(text):
    """
    Extract known skills from resume text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS_DATABASE:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills