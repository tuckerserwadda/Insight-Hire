from typing import Dict, Any
from uuid import uuid4
from datetime import datetime, timezone

JOB_DESCRIPTION_STORE: Dict[str, Dict[str, Any]] = {}

def store_description(doc_type: str, payload: Dict[str, Any], meta: Dict[str, Any]) -> str:
    description_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()

    JOB_DESCRIPTION_STORE[description_id] = {
        'id': description_id,
        'doc_type': doc_type,
        'created_at': now,
        'meta': meta,
        'payload': payload,
    }
    return description_id

def get_description(description_id: str) -> Dict[str, Any] | None:
    return JOB_DESCRIPTION_STORE.get(description_id)