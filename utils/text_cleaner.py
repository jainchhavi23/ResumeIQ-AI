import re


def clean_text(text):
    # Remove extra spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces from beginning and end of lines
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines)