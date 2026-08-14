from flask import Blueprint, request
import os

from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from services.resume_parser import parse_resume
from services.skills_extractor import extract_skills


upload = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"


@upload.route("/analyze", methods=["POST"])
def analyze():

    # ---------------------------------------
    # 1. Check if resume was uploaded
    # ---------------------------------------

    if "resume" not in request.files:
        return "Please select a resume."

    resume = request.files["resume"]

    # ---------------------------------------
    # 2. Check filename
    # ---------------------------------------

    if resume.filename == "":
        return "Please select a resume."

    # ---------------------------------------
    # 3. Check file type
    # ---------------------------------------

    if not resume.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."

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
    # 6. Extract text from PDF
    # ---------------------------------------

    resume_text = extract_text_from_pdf(file_path)

    # ---------------------------------------
    # 7. Clean extracted text
    # ---------------------------------------

    cleaned_text = clean_text(resume_text)

    # ---------------------------------------
    # 8. Extract basic resume information
    # ---------------------------------------

    resume_data = parse_resume(cleaned_text)

    # ---------------------------------------
    # 9. Extract skills
    # ---------------------------------------

    skills = extract_skills(cleaned_text)

    # ---------------------------------------
    # 10. Convert skills into HTML
    # ---------------------------------------

    skills_html = ""

    for skill in skills:
        skills_html += f"""
        <span class="skill-tag">
            {skill.title()}
        </span>
        """

    # ---------------------------------------
    # 11. Return analysis result
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
                color: #ffffff;
                font-family: Arial, sans-serif;
                min-height: 100vh;
                padding: 40px;
            }}


            .container {{
                max-width: 1100px;
                margin: auto;
            }}


            /* Header */

            .header {{
                margin-bottom: 35px;
            }}


            .header h1 {{
                font-size: 36px;
                margin-bottom: 10px;
            }}


            .header h1 span {{
                color: #8b5cf6;
            }}


            .header p {{
                color: #94a3b8;
                font-size: 16px;
            }}


            /* Cards */

            .card {{
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 16px;
                padding: 25px;
                margin-bottom: 25px;
            }}


            .card h2 {{
                color: #ffffff;
                margin-bottom: 20px;
                font-size: 21px;
            }}


            /* Information grid */

            .info-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }}


            .info-item {{
                background: #0b1220;
                padding: 16px;
                border-radius: 10px;
                border: 1px solid #1e293b;
            }}


            .info-label {{
                color: #94a3b8;
                font-size: 13px;
                margin-bottom: 6px;
            }}


            .info-value {{
                color: #ffffff;
                font-size: 15px;
                word-break: break-word;
            }}


            /* Skills */

            .skills-count {{
                color: #94a3b8;
                margin-bottom: 15px;
            }}


            .skill-tag {{
                display: inline-block;
                background: #312e81;
                color: #ddd6fe;
                border: 1px solid #4c1d95;
                padding: 8px 13px;
                margin: 5px;
                border-radius: 20px;
                font-size: 14px;
            }}


            /* Resume text */

            .resume-text {{
                background: #080d18;
                border: 1px solid #1f2937;
                border-radius: 10px;
                padding: 20px;
                white-space: pre-wrap;
                word-wrap: break-word;
                line-height: 1.7;
                color: #cbd5e1;
                max-height: 600px;
                overflow-y: auto;
            }}


            /* Back button */

            .back-btn {{
                display: inline-block;
                text-decoration: none;
                background: #7c3aed;
                color: white;
                padding: 12px 22px;
                border-radius: 9px;
                margin-top: 5px;
                transition: 0.2s;
            }}


            .back-btn:hover {{
                background: #8b5cf6;
            }}


            /* Responsive */

            @media (max-width: 700px) {{

                body {{
                    padding: 20px;
                }}

                .info-grid {{
                    grid-template-columns: 1fr;
                }}

                .header h1 {{
                    font-size: 28px;
                }}

            }}

        </style>

    </head>


    <body>

        <div class="container">


            <!-- Header -->

            <div class="header">

                <h1>
                    Resume<span>IQ</span> AI
                </h1>

                <p>
                    Resume analysis completed successfully.
                </p>

            </div>



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



            <!-- Skills -->

            <div class="card">

                <h2>
                    Skills Found
                </h2>

                <p class="skills-count">

                    Total Skills Found:
                    <strong>{len(skills)}</strong>

                </p>


                <div>

                    {skills_html if skills_html else
                    '<p style="color:#94a3b8;">No skills detected.</p>'}

                </div>

            </div>



            <!-- Resume Text -->

            <div class="card">

                <h2>
                    Extracted Resume Text
                </h2>

                <div class="resume-text">
                    {cleaned_text}
                </div>

            </div>



            <!-- Back -->

            <a href="/" class="back-btn">
                ← Back to Dashboard
            </a>


        </div>

    </body>

    </html>
    """