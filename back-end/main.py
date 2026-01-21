from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from xml.dom.minidom import Document
from docx import Document
from io import BytesIO
from typing import List
from routers.description import router as description_router
 
insight_hire_app = FastAPI(title = 'InsightHire')

# allow frontend requests
origins = [
    'http://localhost:5173'
    'http://127.0.0.1:5173/'
]

insight_hire_app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"]

)

# check server health api
@insight_hire_app.get('/server')
def api_check():
    return({'status': 200, 'message': 'The api is working correctly'})


#include routers

insight_hire_app.include_router(description_router)
# upload file 

TYPES_ALLOWED = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
]

MAX_FiLE_SIZE = 10

#upload file
@insight_hire_app.post('/resume/upload')
async def resume_upload(file:UploadFile = File(...)):
    if file.content_type not in TYPES_ALLOWED:
        raise HTTPException(
            status_code = 400,
            detail = ' Only PDF and word documents allowed'
        )
 # check file and size
    file_data = await file.read()
    size = len(file_data) / (1024 * 1024)
    if size > MAX_FiLE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f'uploaded file is too large. maximum size allowed {MAX_FiLE_SIZE} mb'
        )
    
    text_content = get_resume_content(file.content_type, file_data)
    if not text_content.strip():
        raise HTTPException(
            status_code=400,
            detail='can not read content from resume'
        )
    skills = get_skills(text_content)
    
    return {
        'filename': file.filename,
        'size': round(size, 2),
        'message':'file has been uploaded sucessfully',
        'skills':skills,
        'skills_length':len(skills),
    } 

# extract skills from uploaded resume 
KEY_WORDS_FOR_SKILLS =[
    'python',
    'nlp',
    'azure',
    'aws',
    'data science',
    'react'
]

# get skills from pdf
def get_pdf_text(file_content:bytes)->str:

    pdf_reader = PdfReader(BytesIO(file_content))
    content_parts = []

    for page in pdf_reader.pages:
        try:
            content_parts.append(page.extract_text() or '')
        except Exception:
            continue
        return '\n'.join(content_parts)
    
    #extract from word docs
def get_doc_text(file_content:bytes)->str:
    document = Document(BytesIO(file_content))
    return '\n'.join(p.text for p in document.paragraphs)


# get resume data 
def get_resume_content(file_content_type: str, file_content: bytes) -> str:
    if file_content_type == 'application/pdf':
        return get_pdf_text(file_content)
    elif file_content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return get_doc_text(file_content)
    
    elif file_content_type == "application/msword":
    #doc files won't parse cleanl
        #  we treat them as unsupported for text extraction
        raise HTTPException(
            status_code=400,
            detail="Legacy .doc files are not fully supported. Please upload PDF or .docx.",
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type for text extraction.",
        ) 
    
    # get skills from extracted text

def get_skills(text: str) -> List[str]:
    lower_text = text.lower()
    found = []
    for skill  in KEY_WORDS_FOR_SKILLS:
        if skill in lower_text:
            found.append(skill)
    # Remove duplicates and keep consistent order
    return sorted(set(found))

