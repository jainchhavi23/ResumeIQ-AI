import os

from flask import Blueprint, render_template, request
from config import Config
from utils.pdf_reader import extract_text
from utils.skills_extractor import extract_skills

upload = Blueprint("upload", __name__)


@upload.route("/upload")
def upload_page():
    return render_template("upload.html")


@upload.route("/analyze", methods=["POST"])
def analyze():

    # Get uploaded resume
    resume = request.files["resume"]

    # Get Job Description
    job_description = request.form["job_description"]

    # Validate file
    if resume.filename == "":
        return "Please upload a resume."

    # Create upload folder if it doesn't exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Save uploaded file
    filepath = os.path.join(Config.UPLOAD_FOLDER, resume.filename)
    resume.save(filepath)

    # Extract text from PDF
    resume_text = extract_text(filepath)

    # Extract skills
    detected_skills = extract_skills(resume_text)

    return render_template(
        "result.html",
        resume_text=resume_text,
        detected_skills=detected_skills,
        job_description=job_description
    )