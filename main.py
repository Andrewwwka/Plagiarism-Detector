from fastapi import FastAPI;
from pydantic import BaseModel;
import database

app = FastAPI(title="AI Plagiarism Checker", description="A simple plagariasm checker powered by AI", version="1.0.0")

# Define the input model for the document
class DocumentInput(BaseModel):
    text: str

# reusable helper function
def preprocess_text(text: str) -> str:
    STOP_WORDS = ["the","is","at","which","on"]
    cleaned_words = []
    for word in text.split():
        cleaned_word = word.lower().strip(" .,!?")
        if cleaned_word not in STOP_WORDS:
            cleaned_words.append(cleaned_word)
    return ' '.join(cleaned_words)


#Function 1: Ingesting the document
@app.post("/add_document")
def add_document(document: DocumentInput):
    raw_text = document.text
    # Here you would typically store the document in a database or perform some processing

    cleaned = preprocess_text(raw_text)

    database.add_document_to_database(raw_text, cleaned)

#Function 2: Checking for plagiarism
@app.post("/check_plagiarism")
def check_plagiarism(document: DocumentInput):
    raw_text = document.text
    # Here you would typically call your plagiarism checking logic

    suspicious_cleaned_text = preprocess_text(raw_text)
    matches = database.scan_database_for_matches(suspicious_cleaned_text)


    # return the matches to the user
    return { "matches": matches, "text_length": len(raw_text) }


