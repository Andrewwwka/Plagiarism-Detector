from fastapi import FastAPI;
from pydantic import BaseModel;
import database

app = FastAPI(title="AI Plagiarism Checker", description="A simple plagariasm checker powered by AI", version="1.0.0")

# Define the input model for the document
class DocumentInput(BaseModel):
    text: str

#Function 1: Ingesting the document
@app.post("/add_document")
def add_document(document: DocumentInput):
    STOP_WORDS = ["the","is","at","which","on"]  # Example list of forbidden words
    raw_text = document.text
    # Here you would typically store the document in a database or perform some processing

    cleaned_words = []
    for word in raw_text.split():
        cleaned_word = word.lower().strip(".,!?;:\"'()[]{}")  # Basic cleaning
        if cleaned_word not in STOP_WORDS: 
            cleaned_words.append(cleaned_word)
    cleaned_text = ' '.join(cleaned_words)

    # For demonstration, we will just return a success message
    return {"message": "Document added successfully", "text_length": len(raw_text)}

#Function 2: Checking for plagiarism
@app.post("/check_plagiarism")
def check_plagiarism(document: DocumentInput):
    raw_text = document.text
    # Here you would typically call your plagiarism checking logic
    
    is_plagiarized = False  # Replace with actual plagiarism checking logic

    return {"is_plagiarized": is_plagiarized, "text_length": len(raw_text)}


