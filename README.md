# LinkedIn Resume Generator using Gemini AI

## Overview

This project is a web application that generates a professional HTML resume from an uploaded PDF file using the Gemini AI model. The application uses FastAPI to create a RESTful API and Jinja2 templates to render the HTML response.

## Approach

To solve this problem, I followed these steps:

1. **Set up the project structure**: Created a new FastAPI project with a `main.py` file and a `templates` directory for the HTML templates.
2. **Define the API endpoint**: Defined a single API endpoint `/generate_resume/` that accepts a PDF file upload and returns an HTML response.
3. **Read and extract text from PDF**: Used the `PyPDF2` library to read the uploaded PDF file and extract the text content.
4. **Generate HTML resume using Gemini AI**: Utilized the Gemini AI model to generate a professional HTML resume from the extracted text. A prompt was crafted to specify the structure and content of the desired HTML resume.
5. **Return the HTML response**: Used the `HTMLResponse` object from FastAPI to return the generated HTML resume as a response to the API request.
6. **Create a home page with a form**: Developed a simple home page with a form that allows users to upload a PDF file and submit it to the `/generate_resume/` endpoint.

## How to Use

1. Run the application by executing `python main.py` in your terminal.
2. Open a web browser and navigate to `http://localhost:8000/`.
3. Click on the "Browse" button to select a PDF file to upload.
4. Click on the "Generate Resume" button to submit the form.
5. The application will generate an HTML resume based on the uploaded PDF file and display it in the browser.

## Technical Details

- The application uses **FastAPI** as the web framework.
- The **Gemini AI** model is used to generate the HTML resume.
- **PyPDF2** is used to read and extract text from the uploaded PDF file.
- **Jinja2** templates are used to render the HTML response.
- The application is configured to use the `GOOGLE_API_KEY` environment variable to authenticate with the Gemini AI API.

---

## openaiversion.py: OpenAI GPT-4 Based Resume Generator

This file contains code for a FastAPI application that generates a professional HTML resume from a PDF file using OpenAI's GPT-4 model.

### Functionality:

1. The user uploads a PDF file and inputs their OpenAI API key on the home page (`/`).
2. The PDF file is read, and its content is extracted using `PyPDF2`.
3. The extracted text is sent to OpenAI's GPT-4 model to generate a professional HTML resume.
4. The generated resume text is parsed to extract dynamic data such as name, email, phone, location, summary, work experience, education, skills, and projects.
5. The extracted data is used to render an HTML template (`resume_template.html`) with the user's information.

### Usage:

1. Save the code in a file (e.g., `app.py`).
2. Install the required libraries by running:
   ```bash
   pip install fastapi openai PyPDF2
3. Create a new file named resume_template.html in a directory named templates (create the directory if it doesn't exist). This template will be used to render the generated resume.
4. Run the application by executing: uvicorn app:app --host 0.0.0.0 --port 8000
5. Open a web browser and navigate to http://localhost:8000 (or the specified port).
6. Upload a PDF file and input your OpenAI API key on the home page.
7. Click the "Generate Resume" button to generate and view your professional HTML resume.
