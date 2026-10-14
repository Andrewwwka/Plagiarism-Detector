from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

app = FastAPI(
    title="AI Plagiarism Checker API",
    description="Sentence-level AI plagiarism detector powered by ChromaDB",
    version="2.0.0"
)

class DocumentInput(BaseModel):
    text: str

class CheckInput(BaseModel):
    text: str
    threshold: float = 0.75

@app.post("/add_document")
def add_document(document: DocumentInput):
    if not document.text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")
    chunks_added = database.save_document_to_database(document.text)
    return {"message": "Document indexed successfully", "chunks_indexed": chunks_added}

@app.post("/check_plagiarism")
def check_plagiarism(payload: CheckInput):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Suspicious text cannot be empty.")
    matches = database.scan_database_for_matches(payload.text, threshold=payload.threshold)
    return {"matches": matches, "text_length": len(payload.text)}

@app.get("/stats")
def get_stats():
    return database.get_database_stats()

@app.delete("/clear")
def clear_db():
    database.clear_database()
    return {"message": "Database cleared successfully."}