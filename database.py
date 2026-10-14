import numpy as py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

DOCUMENT_DATABASE = []

# saves the document to the database with its vector representation
def save_document_to_database(raw_text: str, cleaned_text: str):
    vector = model.encode(cleaned_text, convert_to_tensor=True)

    document_entry = {
        "raw": raw_text,
        "text": cleaned_text,
        "vector": vector
    }
    
    DOCUMENT_DATABASE.append(document_entry)

#compares the suspicious text to the database and returns matches above a certain threshold
def scan_database_for_matches(suspicious_text: str):
    suspicious_vector = model.encode(suspicious_text, convert_to_tensor=True)
    
    matches = []
    for document in DOCUMENT_DATABASE:
        stored_vector = document["embedding"]
        similarity_tensor = util.cos_sim(suspicious_vector, stored_vector)
        similarity = similarity_tensor.item()  # Convert tensor to a float value
        if similarity > 0.8:  # Example threshold for plagiarism
            matches.append({
                "raw": document["raw"],
                "cleaned": document["cleaned"],
                "similarity": round(imilarity * 100, 2)
            })
    
    return matches