import streamlit as st
import requests
from pypdf import PdfReader
import os

# Automatically detect if running inside Docker or locally
BACKEND_HOST = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
BACKEND_ADD = f"{BACKEND_HOST}/add_document"
BACKEND_CHECK = f"{BACKEND_HOST}/check_plagiarism"
BACKEND_STATS = f"{BACKEND_HOST}/stats"
BACKEND_CLEAR = f"{BACKEND_HOST}/clear"

st.set_page_config(page_title="AI Plagiarism Detector", page_icon="🛡️", layout="wide")

# Sidebar Controls
st.sidebar.header("Configuration & Stats")

threshold_pct = st.sidebar.slider("Similarity Threshold (%)", min_value=50, max_value=95, value=75, step=5)
threshold_val = threshold_pct / 100.0

st.sidebar.divider()

# Fetch and display database stats
try:
    stats_res = requests.get(BACKEND_STATS, timeout=2)
    if stats_res.status_code == 200:
        stats = stats_res.json()
        st.sidebar.metric("Indexed Sentence Chunks", stats.get("total_chunks", 0))
except:
    st.sidebar.warning("Backend offline or connecting...")

if st.sidebar.button("Clear Database", type="secondary"):
    try:
        res = requests.delete(BACKEND_CLEAR)
        if res.status_code == 200:
            st.sidebar.success("Database cleared!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Main Layout
st.title("AI-Powered Plagiarism Detector")
st.write("Index reference documents and audit suspicious student work with semantic sentence-level matching.")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Index Source Material")
    input_method = st.radio("Input method:", ["Paste Text", "Upload File (.txt, .pdf)"], horizontal=True)
    
    source_text = ""
    if input_method == "Paste Text":
        source_text = st.text_area("Paste reference text here:", height=220, placeholder="Enter official source document...")
    else:
        uploaded_file = st.file_uploader("Upload reference file", type=["txt", "pdf"])
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                source_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
            else:
                source_text = uploaded_file.getvalue().decode("utf-8")
            st.text_area("Extracted Preview:", value=source_text[:400] + "..." if len(source_text) > 400 else source_text, height=130, disabled=True)

    if st.button("Index Document", type="primary"):
        if source_text.strip():
            try:
                response = requests.post(BACKEND_ADD, json={"text": source_text})
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Success! Indexed {data.get('chunks_indexed', 0)} sentence chunks.")
                    st.rerun()
                else:
                    st.error(f"Failed to index: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please provide text to index.")

with col2:
    st.subheader("🔍 Audit Suspicious Document")
    suspicious_text = st.text_area("Paste suspicious text here:", height=270, placeholder="Paste essay or paper to check...")

    if st.button("Run Plagiarism Audit", type="primary"):
        if suspicious_text.strip():
            try:
                response = requests.post(BACKEND_CHECK, json={"text": suspicious_text, "threshold": threshold_val})
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    if not matches:
                        st.info("No plagiarism detected above the threshold.")
                    else:
                        st.error(f"⚠️ Plagiarism Alert! Found {len(matches)} matching segment(s).")
                        
                        for idx, match in enumerate(matches, 1):
                            with st.container():
                                st.markdown(f"**Match #{idx} — Similarity: `{match['similarity']}%`**")
                                st.markdown(f"> **Suspicious Sentence:** `{match['suspicious_sentence']}`")
                                st.markdown(f"> **Matched Source:** `{match['matched_sentence']}`")
                                st.divider()
                else:
                    st.error(f"Audit failed: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please provide text to audit.")