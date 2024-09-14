from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
from PyPDF2 import PdfReader
from io import BytesIO
import re

app = FastAPI()

# Initialize Jinja2 template directory
templates = Jinja2Templates(directory="templates")

def extract_resume_data(resume_text):
    # Use regex or simple text processing to extract fields from the OpenAI-generated resume text
    name = re.search(r'Name[:\-]\s*(.*)', resume_text)
    email = re.search(r'Email[:\-]\s*(.*)', resume_text)
    phone = re.search(r'Phone[:\-]\s*(.*)', resume_text)
    location = re.search(r'Location[:\-]\s*(.*)', resume_text)
    summary = re.search(r'Summary[:\-]\s*(.*)', resume_text)
    
    # Example extraction for work experience (expandable)
    work_experience = []
    work_exp_matches = re.findall(r'(\w+\s\w+) at ([\w\s]+) \(([\w\s]+) - ([\w\s]+)\): (.*)', resume_text)
    for match in work_exp_matches:
        work_experience.append({
            "title": match[0],
            "company": match[1],
            "start_date": match[2],
            "end_date": match[3],
            "description": match[4]
        })

    # Example extraction for education
    education = []
    edu_matches = re.findall(r'Degree[:\-]\s*(.*) from (.*) \((\d{4})\)', resume_text)
    for match in edu_matches:
        education.append({
            "degree": match[0],
            "institution": match[1],
            "graduation_year": match[2]
        })

    # Example extraction for skills
    skills = re.findall(r'Skill[:\-]\s*(.*)', resume_text)

    # Example extraction for projects
    projects = []
    project_matches = re.findall(r'Project[:\-]\s*(.*)\nDescription[:\-]\s*(.*)', resume_text)
    for match in project_matches:
        projects.append({
            "name": match[0],
            "description": match[1]
        })

    return {
        "name": name.group(1) if name else "John Doe",
        "email": email.group(1) if email else "john.doe@example.com",
        "phone": phone.group(1) if phone else "+123456789",
        "location": location.group(1) if location else "New York, USA",
        "summary": summary.group(1) if summary else "A professional with diverse experience.",
        "work_experience": work_experience if work_experience else [
            {"title": "Software Engineer", "company": "Tech Corp", "start_date": "Jan 2020", "end_date": "Present", "description": "Developed scalable systems."},
        ],
        "education": education if education else [
            {"degree": "B.Sc. Computer Science", "institution": "VIT Vellore", "graduation_year": "2024"}
        ],
        "skills": skills if skills else ["Python", "FastAPI", "Machine Learning"],
        "projects": projects if projects else [{"name": "AI Resume Generator", "description": "Built a web app that generates resumes."}]
    }

@app.post("/generate_resume/")
async def generate_resume(request: Request, file: UploadFile = File(...), api_key: str = Form(...)):
    # Set the OpenAI API key provided by the user
    openai.api_key = api_key

    # Read the content of the uploaded PDF
    content = await file.read()
    reader = PdfReader(BytesIO(content))
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Use OpenAI API to generate resume details from the extracted text
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"""
            Extract the key details from the following text and format it into a professional HTML resume. 
            The structure should include: 

            1. Name and contact information
            2. Summary/Objective section
            3. Work experience, with job titles, company names, dates, and descriptions
            4. Education, including degrees, institutions, and graduation dates
            5. Skills section, with relevant technical and soft skills
            6. Additional sections like certifications, projects, or awards (if applicable)

            Text content: {text}
        """,
        max_tokens=1500,
        temperature=0.7
    )

    # Extract the resume text from the OpenAI API response
    resume_text = response.choices[0].text.strip()

    # Extract dynamic resume data from the OpenAI-generated text
    resume_data = extract_resume_data(resume_text)

    # Return the rendered HTML response using the Jinja2 template
    return templates.TemplateResponse("resume_template.html", {"request": request, **resume_data})

@app.get("/")
async def index():
    # Home page with a form to upload PDF and input OpenAI API key
    return HTMLResponse(content='''
        <html>
        <body>
        <h1>LinkedIn Resume Generator</h1>
        <form action="/generate_resume/" enctype="multipart/form-data" method="post">
        <input name="file" type="file" accept="application/pdf"/>
        <input name="api_key" type="password" placeholder="OpenAI API Key"/>
        <input type="submit" value="Generate Resume"/>
        </form>
        </body>
        </html>
    ''')
