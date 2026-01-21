from fastapi import APIRouter, HTTPException
from schemas.description import JobDescription
from services.processing import description_pipeline
from services.storage import store_description

router = APIRouter(prefix="/job", tags=["Job Description"])

@router.post("/ingest")
async def job_description(req: JobDescription):
    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Job description text is too short.")

    processed = description_pipeline(req.text)

    meta = {
        "title": req.title,
        "company": req.company,
        "source": "frontend_text",
    }

    description_id = store_description("job_description", processed, meta)

    return {
        "status": 200,
        "message": "Job description ingested successfully",
        "ingestion_id": description_id,
    }