from io import BytesIO
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PyPDF2 import PdfReader
import os
import google.generativeai as genai
import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")

os.environ['GOOGLE_API_KEY'] = "AIzaSyDuxIhriLzBt1ifMh9jl5Dh6yBt6wFZHWA"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')


@app.post("/generate_resume/")
async def generate_resume(request: Request, file: UploadFile = File(...)):
    # Read the content of the uploaded PDF
    content = await file.read()
    reader = PdfReader(BytesIO(content))
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Use Gemini API to generate HTML resume from the extracted text
    prompt = f"""
        Generate a professional well structured and defined HTML(code) resume from the following text.
        Elaborate, add metrics(numeric), and make it professional.
        The structure should include: 

        1. Name and contact information
        2. Summary/Objective section
        3. Work experience, with job titles, company names, dates, and descriptions
        4. Education, including degrees, institutions, and graduation dates
        5. Skills section, with relevant technical and soft skills
        6. Additional sections like certifications, projects, or awards (if applicable)

        Text content: {text}
    """
    response = model.generate_content(prompt)
    html_resume = response.text.strip()

    # Return the rendered HTML response using the Gemini-generated HTML
    return HTMLResponse(content=html_resume, media_type="text/html")


@app.get("/")
async def index():
    # Home page with a form to upload PDF
    return HTMLResponse(content='''
        <html>
        <body>
        <h1>LinkedIn Resume Generator</h1>
        <form action="/generate_resume/" enctype="multipart/form-data" method="post">
        <input name="file" type="file" accept="application/pdf"/>
        <input type="submit" value="Generate Resume"/>
        </form>
        </body>
        </html>
    ''')
