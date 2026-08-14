import re


# Skills that ResumeIQ can currently recognize
SKILLS_DATABASE = [
    # Programming Languages
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "sql",

    # Web Development
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

    # Databases
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
    Find known skills inside resume text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS_DATABASE:

        # Escape special characters such as C++
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills