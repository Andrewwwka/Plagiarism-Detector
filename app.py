import streamlit as st
import requests

import streamlit as st
import requests

# FIXED: Complete the local IP configurations with port 8000 and the correct endpoints
BACKEND_URL = "http://127.0.0.1:8000/add_document"
CHECK_URL = "http://127.0.0.1:8000/check_plagiarism"

st.set_page_config(page_title="Plagiarism Detector", page_icon=":guardsman:", layout="wide")


st.title("Plagiarism Detector")
st.write("Upload a document to check for plagiarism.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Document")
    source_text = st.text_area("Or paste text here:", height=200)

    if st.button("Index Source Material"):
        if source_text.strip():
            payload = {"text": source_text} # FIXED: Removed extra colon from key

            try:
                # FIXED: Removed trailing "/index" string manipulation
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    st.success("Document indexed successfully.")
                else:
                    st.error(f"Failed to index document. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while connecting to the backend: {e}")
        else:
            st.warning("Please provide source text to index.")

with col2:
    st.subheader("Audit Suspicious Document")
    suspicious_text = st.text_area("Paste suspicious text here:", height=200, placeholder="Paste suspicious text here...")

    if st.button("Run Plagiarism Check"):
        if suspicious_text.strip():
            payload = {"text": suspicious_text}

            try:
                response = requests.post(CHECK_URL, json=payload)
                if response.status_code == 200:
                    data = response.json() # FIXED: Added parsing assignment
                    matches = data.get("matches", [])
                    if not matches:
                        st.info("No plagiarism detected.")
                    else:
                        st.error("Plagiarism detected") # Changed to error alert for visibility
                        for match in matches:
                            st.write(f"**Matched Text:** {match['cleaned']}")
                            st.write(f"**Similarity:** {match['similarity']}%")
                else:
                    st.error(f"Failed to check for plagiarism. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while connecting to the backend: {e}")
        else:
            st.warning("Please provide suspicious text to check for plagiarism.")
