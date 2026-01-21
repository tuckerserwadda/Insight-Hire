from pydantic import BaseModel, Field
from typing import Optional

class JobDescription(BaseModel):
    text: str = Field(..., min_length=10, description='job description')
    title: Optional[str] = None
    company: Optional[str] = None
    