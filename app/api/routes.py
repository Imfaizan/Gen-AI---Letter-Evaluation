from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.document_chain import evaluate_letter
from app.core.embedding import ingest_policy_documents
import os

router = APIRouter()

@router.post("/ingest/")
async def ingest_documents(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join("/tmp", file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    ingest_policy_documents(file_path)
    return {"message": "Policy document ingested successfully."}

@router.post("/evaluate/")
async def evaluate_letter(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join("/tmp", file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    response = evaluate_letter(file_path)
    return {"highlighted_letter": response}
