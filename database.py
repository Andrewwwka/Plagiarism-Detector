import chromadb
from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
import uuid

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="plagiarism_documents",
    metadata={"hnsw:space": "cosine"}
)

def chunk_text(text: str):
    #splits the text into clean sentences for granular plagiarism checks
    return [s.strip() for s in sent_tokenize(text) if len(s.strip()) > 10]

# saves the document to the database with its vector representation
def save_document_to_database(raw_text: str):
    sentences = chunk_text(raw_text)
    if not sentences:
        return 0
    
    doc_uuid = str(uuid.uuid4())
    embeddings = model.encode(sentences).tolist()
    ids = [f"{doc_uuid}_{i}" for i in range(len(sentences))]
    metadatas = [{"source_sentence": s} for s in sentences]

    collection.add(
        documents=sentences,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    return len(sentences)

#compares the suspicious text to the database and returns matches above a certain threshold
def scan_database_for_matches(suspicious_text: str, threshold: float = 0.75):
    sentences = chunk_text(suspicious_text)
    if not sentences:
        return []

    embeddings = model.encode(sentences).tolist()

    results = collection.query(
        query_embeddings=embeddings,
        n_results=1
    )
    matches = []
    if results and results['distances']:
        for i, sent in enumerate(results[sentences]):
            distances = results['distances'][i]
            metadatas = results['metadatas'][i]

            if distances and metadatas:
                cosine_distance = distances[0]
                similarity = 1.0 - cosine_distance

                if similarity >= threshold:
                    matches.append({
                        "suspicious_sentence": sentences[i],
                        "matched_sentence": metadatas[0]['source_sentence'],
                        "similarity": similarity
                    })
    return matches


def get_database_stats():
    return {"total_chunks": collection.count()}

def clear_database():
    client.delete_collection(name="plagiarism_documents")
    global collection
    collection = client.get_or_create_collection(
        name="plagiarism_documents",
        metadata={"hnsw:space": "cosine"}
    )  
    return True