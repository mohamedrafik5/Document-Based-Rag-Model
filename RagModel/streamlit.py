import requests
import streamlit as st
import hashlib

API_URL = "http://localhost:8000/rag"  # change if needed

st.set_page_config(page_title="RAG PDF Chatbot", layout="centered")

st.title("📄 AI PDF Chatbot")
st.write("Upload a PDF and ask questions about it — with follow-up support.")


# ============================
# Helpers
# ============================

def hash_pdf(file_bytes: bytes):
    """Return SHA256 hash of uploaded PDF."""
    return hashlib.sha256(file_bytes).hexdigest()


# Init session state
if "pdf_hash" not in st.session_state:
    st.session_state.pdf_hash = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================
# PDF Upload Section
# ============================
with st.sidebar:
    st.header("📤 Upload a PDF")

    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file:
        pdf_bytes = uploaded_file.read()
        new_hash = hash_pdf(pdf_bytes)

        # Only upload if the PDF has changed
        if st.session_state.pdf_hash != new_hash:
            # New PDF → clear chat & update hash
            st.session_state.messages = []
            st.session_state.pdf_hash = new_hash

            with st.spinner("Uploading and indexing PDF..."):
                files = {
                    "file": (uploaded_file.name, pdf_bytes, "application/pdf")
                }
                response = requests.post(f"{API_URL}/upload", files=files)

            if response.status_code == 200:
                st.success("PDF uploaded and FAISS index rebuilt! 👍")
            else:
                st.error("Upload failed: " + response.text)

        # If same PDF → do nothing (NO message)


# ============================
# Chat Interface
# ============================

st.subheader("💬 Ask a Question")

# Show chat history
for role, text in st.session_state.messages:
    st.chat_message(role).write(text)

# Chat input logic
if prompt := st.chat_input("Ask anything about the document..."):

    # Save user message
    st.session_state.messages.append(("user", prompt))
    st.chat_message("user").write(prompt)

    # Send question to API
    with st.spinner("Thinking..."):
        response = requests.post(
            f"{API_URL}/query",
            json={"question": prompt}
        )

    if response.status_code == 200:
        answer = response.json().get("answer", "No answer returned.")
    else:
        answer = "Error: " + response.text

    # Save assistant response
    st.session_state.messages.append(("assistant", answer))
    st.chat_message("assistant").write(answer)



# streamlit run RagModel\streamlit.py