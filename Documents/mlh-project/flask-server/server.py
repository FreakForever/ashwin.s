from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS

load_dotenv()  # Load the environment variables
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

@app.route('/process_resume', methods=['POST'])
def process_resume():
    job_description = request.form.get('job_description')
    uploaded_file = request.files.get('resume')

    if not job_description or not uploaded_file:
        return jsonify({'error': 'Missing job description or resume'}), 400

    resume_text = input_pdf_text(uploaded_file)
    input_prompts_template = """
    Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide the best assistance for improving the resumes. Assign the percentage matching based on the JD and the missing keywords with high accuracy.

    resume = {resume_text}
    JD = {job_description}

    I want the response in the form of JSON.
    {{
        "match_percentage": "{{calculated_match_percentage}}",
        "highlighted_resume": "{{highlighted_resume_text}}",
        "suggestions": {{
            "summary_section": {{
                "suggestions": [
                    "Include specific keywords such as 'scalable models' and 'model performance evaluation'."
                ]
            }},
            "experience_section": {{
                "suggestions": [
                    "Emphasize responsibilities like 'designing scalable models' and 'model evaluation'.",
                    "Mention any specific achievements or projects related to these responsibilities."
                ]
            }},
            "skills_section": {{
                "suggestions": [
                    "Add 'Model Evaluation' and 'Feature Engineering' to align with the job description."
                ]
            }},
            "education_section": {{
                "suggestions": [
                    "Consider adding any relevant coursework or projects."
                ]
            }},
            "general_tips": {{
                "formatting": [
                    "Ensure consistent font and bullet point style."
                ],
                "clarity": [
                    "Use bullet points for responsibilities and achievements."
                ],
                "conciseness": [
                    "Keep each bullet point to one or two lines for readability."
                ]
            }}
        }}
    }}
    """

    input_prompts = input_prompts_template.format(resume_text=resume_text, job_description=job_description)
    response = get_gemini_response(input_prompts)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
