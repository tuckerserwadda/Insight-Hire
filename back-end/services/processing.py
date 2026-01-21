import re
import unicodedata
from typing import Dict, Any, List

_whitespace_re = re.compile(r'\s+')
_none_word_re = re.compile((r"[^\w\s\+\#\.\-]"))

def normalize_description(description:str) -> str:
    description = unicodedata.normalize('NFKC', description)
    description = description.replace('\x00', '')
    description = _whitespace_re.sub('', description).strip()
    return description
    
def clean_description(description: str) -> str:
    description = normalize_description(description)
    description = _none_word_re.sub(" ", description)
    description = _whitespace_re.sub(" ", description).strip()
    return description

def tokenize(description: str) -> List[str]:
    if not description:
        return []
    return description.lower().split()

def description_pipeline(raw_description: str) -> Dict[str, Any]:
    cleaned = clean_description(raw_description)
    tokens = tokenize(cleaned)
    return {
        "raw_description": raw_description,
        "cleaned_description": cleaned,
        "tokens": tokens,
    }