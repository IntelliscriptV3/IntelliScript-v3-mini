import os
from datetime import datetime
from fastapi import UploadFile, HTTPException
from ..core.config import settings

def save_upload(file: UploadFile, subdir: str) -> str:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    base = settings.FILE_STORE
    os.makedirs(os.path.join(base, subdir), exist_ok=True)
    safe_name = f"{datetime.utcnow().timestamp()}_{file.filename.replace(' ', '_')}"
    path = os.path.join(base, subdir, safe_name)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path
