import pdfplumber
import docx

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def analyze_resume(text):
    skills_keywords = ["python", "django", "react", "sql", "docker", "vue", "javascript"]
    experience_keywords = ["experience", "worked", "project", "team", "responsible"]
    education_keywords = ["university", "bachelor", "master", "degree", "education"]

    skills = [kw for kw in skills_keywords if kw.lower() in text.lower()]
    experience = [line for line in text.splitlines() if any(kw in line.lower() for kw in experience_keywords)]
    education = [line for line in text.splitlines() if any(kw in line.lower() for kw in education_keywords)]

    return {
        "skills": skills,
        "experience": experience,
        "education": education
    }
