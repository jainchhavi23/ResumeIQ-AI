from flask import Blueprint, request
import os

from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from services.resume_parser import parse_resume
from services.skills_extractor import extract_skills
from services.jd_analyzer import extract_jd_skills
from services.ats_scorer import calculate_ats_score
from services.suggestions import generate_suggestions
from services.section_analyzer import analyze_sections


upload = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"


@upload.route("/analyze", methods=["POST"])
def analyze():

    # ---------------------------------------
    # 1. Check resume
    # ---------------------------------------

    if "resume" not in request.files:
        return "Please select a resume."

    resume = request.files["resume"]

    if resume.filename == "":
        return "Please select a resume."

    # ---------------------------------------
    # 2. Check PDF
    # ---------------------------------------

    if not resume.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."

    # ---------------------------------------
    # 3. Get Job Description
    # ---------------------------------------

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    if not job_description:
        return "Please enter a job description."

    # ---------------------------------------
    # 4. Create uploads folder
    # ---------------------------------------

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # ---------------------------------------
    # 5. Save resume
    # ---------------------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        resume.filename
    )

    resume.save(file_path)

    # ---------------------------------------
    # 6. Extract PDF text
    # ---------------------------------------

    resume_text = extract_text_from_pdf(file_path)

    # ---------------------------------------
    # 7. Clean text
    # ---------------------------------------

    cleaned_text = clean_text(resume_text)

    # ---------------------------------------
    # 8. Parse resume
    # ---------------------------------------

    resume_data = parse_resume(cleaned_text)
sections = analyze_sections(cleaned_text)
section_html = ""

for section, found in sections.items():

    if found:
        status = "✓"
        class_name = "section-found"
    else:
        status = "✗"
        class_name = "section-missing"

    section_html += f"""
    <div class="section-item {class_name}">
        <span>{status}</span>
        <span>{section}</span>
    </div>
    """
    # ---------------------------------------
    # 9. Extract resume skills
    # ---------------------------------------

    skills = extract_skills(cleaned_text)

    # ---------------------------------------
    # 10. Extract JD skills
    # ---------------------------------------

    jd_skills = extract_jd_skills(job_description)

    # ---------------------------------------
    # 11. Matched skills
    # ---------------------------------------

    matched_skills = list(
        set(skills) & set(jd_skills)
    )

    # ---------------------------------------
    # 12. Missing skills
    # ---------------------------------------

    missing_skills = list(
        set(jd_skills) - set(skills)
    )

    # ---------------------------------------
    # 13. Match percentage
    # ---------------------------------------

    if jd_skills:
        match_percentage = round(
            (len(matched_skills) / len(jd_skills)) * 100
        )
    else:
        match_percentage = 0

    # ---------------------------------------
    # 14. ATS score
    # ---------------------------------------

    ats_score = calculate_ats_score(
        cleaned_text,
        resume_data,
        matched_skills,
        jd_skills
    )

    # ---------------------------------------
    # 15. Generate suggestions
    # ---------------------------------------

    suggestions = generate_suggestions(
        resume_data,
        matched_skills,
        missing_skills,
        cleaned_text
    )

    # ---------------------------------------
    # 16. Resume skills HTML
    # ---------------------------------------

    skills_html = ""

    for skill in skills:
        skills_html += f"""
        <span class="skill-tag">
            {skill.title()}
        </span>
        """

    # ---------------------------------------
    # 17. Matched skills HTML
    # ---------------------------------------

    matched_html = ""

    for skill in matched_skills:
        matched_html += f"""
        <span class="matched-tag">
            ✓ {skill.title()}
        </span>
        """

    # ---------------------------------------
    # 18. Missing skills HTML
    # ---------------------------------------

    missing_html = ""

    for skill in missing_skills:
        missing_html += f"""
        <span class="missing-tag">
            ✗ {skill.title()}
        </span>
        """

    # ---------------------------------------
    # 19. Suggestions HTML
    # ---------------------------------------

    suggestions_html = ""

    for suggestion in suggestions:
        suggestions_html += f"""
        <div class="suggestion-item">
            💡 {suggestion}
        </div>
        """

    # ---------------------------------------
    # 20. Score message
    # ---------------------------------------

    if match_percentage >= 80:
        score_message = "Excellent match for this job!"

    elif match_percentage >= 60:
        score_message = (
            "Good match, but some skills can be improved."
        )

    elif match_percentage >= 40:
        score_message = (
            "Moderate match. Consider improving missing skills."
        )

    else:
        score_message = (
            "Low match. More relevant skills may be required."
        )

    # ---------------------------------------
    # 21. Result page
    # ---------------------------------------

    return f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Resume Analysis - ResumeIQ AI</title>

        <style>

            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                background: #080d18;
                color: white;
                font-family: Arial, sans-serif;
                min-height: 100vh;
                padding: 40px;
            }}

            .container {{
                max-width: 1100px;
                margin: auto;
            }}

            h1 {{
                margin-bottom: 10px;
                font-size: 36px;
            }}

            h1 span {{
                color: #8b5cf6;
            }}

            .subtitle {{
                color: #94a3b8;
                margin-bottom: 30px;
            }}

            .card {{
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 16px;
                padding: 25px;
                margin-bottom: 25px;
            }}

            .card h2 {{
                margin-bottom: 20px;
            }}

            .info-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }}

            .info-item {{
                background: #0b1220;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #1e293b;
            }}

            .info-label {{
                color: #94a3b8;
                font-size: 13px;
                margin-bottom: 6px;
            }}

            .info-value {{
                color: white;
                word-break: break-word;
            }}

            .skill-tag {{
                display: inline-block;
                background: #312e81;
                color: #ddd6fe;
                padding: 8px 13px;
                margin: 5px;
                border-radius: 20px;
                font-size: 14px;
            }}

            .matched-tag {{
                display: inline-block;
                background: #064e3b;
                color: #6ee7b7;
                border: 1px solid #065f46;
                padding: 8px 13px;
                margin: 5px;
                border-radius: 20px;
                font-size: 14px;
            }}

            .missing-tag {{
                display: inline-block;
                background: #450a0a;
                color: #fca5a5;
                border: 1px solid #7f1d1d;
                padding: 8px 13px;
                margin: 5px;
                border-radius: 20px;
                font-size: 14px;
            }}

            .job-description {{
                background: #080d18;
                border: 1px solid #1f2937;
                border-radius: 10px;
                padding: 20px;
                white-space: pre-wrap;
                line-height: 1.7;
                color: #cbd5e1;
            }}

            .match-score {{
                font-size: 48px;
                font-weight: bold;
                color: #8b5cf6;
                margin-bottom: 10px;
            }}

            .score-message {{
                color: #94a3b8;
                margin-bottom: 25px;
            }}

            .progress-container {{
                width: 100%;
                height: 12px;
                background: #1e293b;
                border-radius: 10px;
                overflow: hidden;
                margin-bottom: 25px;
            }}

            .progress-bar {{
                height: 100%;
                width: {match_percentage}%;
                background: #8b5cf6;
                border-radius: 10px;
            }}

            .skill-section {{
                margin-bottom: 25px;
            }}

            .section-title {{
                margin-bottom: 10px;
                font-size: 17px;
            }}

            .suggestion-item {{
                background: #0b1220;
                border: 1px solid #1e293b;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                color: #cbd5e1;
                line-height: 1.5;
            }}

            .resume-text {{
                background: #080d18;
                border: 1px solid #1f2937;
                border-radius: 10px;
                padding: 20px;
                white-space: pre-wrap;
                line-height: 1.7;
                color: #cbd5e1;
                max-height: 500px;
                overflow-y: auto;
            }}

            .back-btn {{
                display: inline-block;
                text-decoration: none;
                background: #7c3aed;
                color: white;
                padding: 12px 22px;
                border-radius: 9px;
            }}

            .back-btn:hover {{
                background: #8b5cf6;
            }}

            @media (max-width: 700px) {{

                body {{
                    padding: 20px;
                }}

                .info-grid {{
                    grid-template-columns: 1fr;
                }}

                h1 {{
                    font-size: 28px;
                }}

            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>
                Resume<span>IQ</span> AI
            </h1>

            <p class="subtitle">
                Resume analysis completed successfully.
            </p>


            <!-- Extracted Information -->

            <div class="card">

                <h2>
                    Extracted Information
                </h2>

                <div class="info-grid">

                    <div class="info-item">
                        <div class="info-label">
                            Name
                        </div>
                        <div class="info-value">
                            {resume_data.get("name") or "Not found"}
                        </div>
                    </div>

                    <div class="info-item">
                        <div class="info-label">
                            Email
                        </div>
                        <div class="info-value">
                            {resume_data.get("email") or "Not found"}
                        </div>
                    </div>

                    <div class="info-item">
                        <div class="info-label">
                            Phone
                        </div>
                        <div class="info-value">
                            {resume_data.get("phone") or "Not found"}
                        </div>
                    </div>

                    <div class="info-item">
                        <div class="info-label">
                            LinkedIn
                        </div>
                        <div class="info-value">
                            {resume_data.get("linkedin") or "Not found"}
                        </div>
                    </div>

                    <div class="info-item">
                        <div class="info-label">
                            GitHub
                        </div>
                        <div class="info-value">
                            {resume_data.get("github") or "Not found"}
                        </div>
                    </div>

                </div>

            </div>


            <!-- Resume Skills -->

            <div class="card">

                <h2>
                    Resume Skills
                </h2>

                <p style="color:#94a3b8; margin-bottom:15px;">
                    Total Skills:
                    <strong>{len(skills)}</strong>
                </p>

                <div>
                    {
                        skills_html
                        if skills_html
                        else
                        '<p style="color:#94a3b8;">No skills detected.</p>'
                    }
                </div>

            </div>


            <!-- Job Description -->

            <div class="card">

                <h2>
                    Job Description
                </h2>

                <div class="job-description">
                    {job_description}
                </div>

            </div>


            <!-- ATS Score -->

            <div class="card">

                <h2>
                    ATS Score
                </h2>

                <div class="match-score">
                    {ats_score}/100
                </div>

                <p class="score-message">
                    ResumeIQ AI ATS-style score based on
                    resume and job requirements.
                </p>

            </div>

<div class="card">

    <h2>
        Resume Section Analysis
    </h2>

    <p style="color:#94a3b8; margin-bottom:20px;">
        Important sections detected in your resume
    </p>

    {section_html}

</div>
            <!-- Job Match Analysis -->

            <div class="card">

                <h2>
                    Job Match Analysis
                </h2>

                <div class="match-score">
                    {match_percentage}%
                </div>

                <p class="score-message">
                    {score_message}
                </p>

                <div class="progress-container">
                    <div class="progress-bar"></div>
                </div>


                <div class="skill-section">

                    <h3 class="section-title">
                        Matched Skills
                    </h3>

                    <div>
                        {
                            matched_html
                            if matched_html
                            else
                            '<p style="color:#94a3b8;">No matching skills found.</p>'
                        }
                    </div>

                </div>


                <div class="skill-section">

                    <h3 class="section-title">
                        Missing Skills
                    </h3>

                    <div>
                        {
                            missing_html
                            if missing_html
                            else
                            '<p style="color:#6ee7b7;">No missing skills 🎉</p>'
                        }
                    </div>

                </div>

            </div>


            <!-- Improvement Suggestions -->

            <div class="card">

                <h2>
                    Resume Improvement Suggestions
                </h2>

                {
                    suggestions_html
                    if suggestions_html
                    else
                    '<p style="color:#6ee7b7;">Your resume looks good! 🎉</p>'
                }

            </div>


            <!-- Extracted Resume Text -->

            <div class="card">

                <h2>
                    Extracted Resume Text
                </h2>

                <div class="resume-text">
                    {cleaned_text}
                </div>

            </div>


            <a href="/" class="back-btn">
                ← Back to Dashboard
            </a>

        </div>

    </body>

    </html>
    """