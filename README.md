# AI-Based Semantic Plagiarism Detector 🛡️

A modern, machine-learning-powered Plagiarism Detection System that moves beyond rigid, word-for-word text matching. By utilizing **Natural Language Processing (NLP)** and **Transformer Embeddings**, this application analyzes the *semantic meaning* of documents—allowing it to catch sophisticated paraphrasing even if two texts use completely different vocabularies.

Built as a decoupled full-stack Python application utilizing a **FastAPI backend engine** and an interactive **Streamlit web frontend dashboard**.

---

## 🚀 Key Features

*   **Semantic AI Analysis:** Powered by Hugging Face's `all-MiniLM-L6-v2` Sentence-BERT model to translate structural text context into numerical vector embeddings.
*   **Intelligent Text Preprocessing:** Custom pipeline that normalizes input text, cleans edge punctuation, and strips high-frequency "stop words" to isolate raw semantic intent.
*   **Vector Engine Verification:** Utilizes Cosine Similarity math to compute exact geometric alignment scores between unknown submissions and indexed source records.
*   **Intuitive Split UI Dashboard:** Clean, user-friendly frontend allowing users to simultaneously build a trusted knowledge base and audit suspicious essays.

---

## 🛠️ Tech Stack & Architecture

The project features a **Decoupled Service Architecture** which enforces clean separation of concerns between web ingestion, routing, and machine learning computation.

*   **Frontend Dashboard:** Streamlit (Python Web Framework)
*   **Backend Server:** FastAPI (High-performance ASGI API framework)
*   **Server Gateway:** Uvicorn
*   **AI Engine:** Sentence-Transformers (Sentence-BERT framework)
*   **Numerical Analytics:** PyTorch & NumPy

