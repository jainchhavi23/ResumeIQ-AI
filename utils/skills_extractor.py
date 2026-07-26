from utils.skills import SKILLS

def extract_skills(text):

    detected = []

    text = text.lower()

    for skill in SKILLS:

        if skill.lower() in text:

            detected.append(skill)

    return detected