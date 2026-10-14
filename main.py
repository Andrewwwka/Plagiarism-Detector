from fastapi import FastAPI;
from pydantic import BaseModel;

app = FastAPI(title="AI Plagiarism Checker", description="A simple plagariasm checker powered by AI", version="1.0.0")

# Define the input model for the document
class DocumentInput(BaseModel):
    text: str

#Function 1: Ingesting the document
@app.post("/add_document")
def add_document(document: DocumentInput):
    raw_text = document.text
    # Here you would typically store the document in a database or perform some processing
    #TO DO add cleanup stuff here
    for word in raw_text.strip().split():
        if word.lower() in ["the", "is", "at", "which", "on"]:
            raw_text = raw_text.replace(word, "")

    return {"message": "Document added successfully", "text_length": len(raw_text)}

@app.post("/check_plagiarism")
def check_plagiarism(document: DocumentInput):
    raw_text = document.text
    # Here you would typically call your plagiarism checking logic
    # For demonstration, we will just return a dummy response


    is_plagiarized = False  # Replace with actual plagiarism checking logic
    return {"is_plagiarized": is_plagiarized, "text_length": len(raw_text)}
