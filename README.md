# 📚 Document-Based RAG Chatbot

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload documents and ask questions based on their content. It leverages semantic search and LLM reasoning to deliver **accurate and context-aware answers** grounded in your own knowledge base.

---

## 🚀 Key Features
- 📄 Upload your own documents for private knowledge querying
- 🔍 **FAISS-based vector search** for efficient document retrieval
- 🧠 **Query Refinement** to enhance retrieval relevance & reduce hallucination
- ⚡ Fast inference powered by **Groq (Llama 3.1)**
- 🎯 Customizable prompt templates for improved response control
- 🧩 Modular architecture — easy to extend and optimize
- 🌐 Simple & interactive **Streamlit UI**
- 🛠 Configurable via `config.yaml`

---

## 🏗️ Project Structure

```bash
RagModel/
│
├─ api/                          # FastAPI endpoints for RAG pipeline
│  └─ endpoint.py                # Handles user query requests
│
├─ config/                       # Configuration & prompt templates
│  ├─ config.yaml                # Model, embeddings & pipeline config
│  └─ prompt.txt                 # Custom prompt for RAG responses
│
├─ core/                         # Core RAG logic
│  └─ model_invoking.py          # LLM invocation & response generation
│
├─ data/                         # Local vector DB & temp file storage
│  ├─ faiss_db/                  # FAISS vector index
│  ├─ file_hashe.txt             # File hash tracker to prevent re-indexing
│  └─ temp_pdf_store.pdf         # Temporary user document storage
│
├─ utils/                        # Utility modules for pipeline support
│  ├─ custom_memory.py           # Conversation memory management
│  ├─ db_manager.py              # Vector DB operations
│  ├─ file_utils.py              # File validation & preprocessing
│  ├─ load_config.py             # Reads & loads YAML configuration
│  └─ query_refiner.py           # Improves queries before retrieval
│
├─ main.py                       # FastAPI backend entrypoint
├─ streamlit.py                  # Streamlit UI for user interaction
└─ .env                          # API keys & env variables (not for commit)
````
---

## 🔧 Tech Stack

| Layer | Technology |
|------|------------|
| LLM | Llama 3.1 (Groq API) |
| Embeddings | All-MiniLM-L6-V2 |
| Vector DB | FAISS |
| Backend | FastAPI |
| Frontend | Streamlit |
| Language | Python 3.10 |

---

## 🧠 Query Refinement (Key Enhancement!)

Your system includes a **Query Refining Layer** to:
- Expand incomplete or vague questions
- Improve semantic matching with document chunks
- Increase retrieval precision
- Reduce LLM hallucination cases

📌 Implemented in: `utils/query_refiner.py`

Example:
> User asks: *"accuracy?"*  
✔ Query Refiner → *"What is the model accuracy mentioned in this document?"*

This greatly elevates RAG performance and reliability.

---
## 🧩 RAG Architecture
```bash
     ┌───────────────────────┐
     │      User Query       │
     └──────────┬────────────┘
                ↓
     ┌───────────────────────┐
     │   Query Refinement    │
     └──────────┬────────────┘
                ↓
     ┌───────────────────────┐
     │     Streamlit UI      │
     └──────────┬────────────┘
                ↓
     ┌───────────────────────┐
     │     FastAPI Backend   │
     └──────────┬────────────┘
                ↓
┌───────────────────────────────────────────┐
│ RAG Core │
│ ┌─────────────┬──────────────┬──────────┐ │
│ │ Embeddings │ Vector Store │ Retriever│ │
│ └─────────────┴──────────────┴──────────┘ │
└─────────────────────────┬─────────────────┘
                ↓
        LLM (Groq - Llama 3.1)
                ↓
            Final Answer

````
---

---

## ⚙️ Configuration

All key behavior is controlled through the config files:

📍 `config/config.yaml`  
📍 `config/prompt.txt`

Includes settings for:
- Chunking strategy
- Embedding model selection
- API keys
- File persistence & paths
- LLM inference parameters

---

## ▶️ How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
---

## 2️⃣ Add your Groq API key to .env
```bash
GROQ_API_KEY=your_key_here
```
## 3️⃣ Launch the Backend (FastAPI)
```bash
python main.py
```
## 4️⃣ Launch the Web UI (Streamlit)
```bash
streamlit run streamlit.py
```
---

## 🧪 Future Enhancements

* Multi-document support

* Advanced long-term memory

* OCR for scanned PDFs

* Cloud deployment with Docker

* Better UI with sidebar file manager
---
## 🤝 Contributing

PRs and suggestions are welcome!
If you find any issues — feel free to report them.

---

## 📄 License

This project is released under the MIT License.
Feel free to use it as a learning resource, a base for your own RAG apps, or internal tools.