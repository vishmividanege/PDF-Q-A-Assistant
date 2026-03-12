# 📄 PDF Q&A Assistant (LLM-Based Document Intelligence)

A simple and clean **PDF Question Answering Assistant** built with **Streamlit**.  
Upload a PDF, process it, and ask questions to get answers based on the document content.

The system uses **retrieval-based question answering with embeddings and a QA chain** to generate accurate responses from the uploaded document.

---

## ✨ Features

-  Upload a PDF file
-  Process PDF (load + split into chunks)
-  Ask questions about the PDF content
-  Retrieval-based answering (context + QA chain)
-  Recent question history (last 10 shown)
-  Download full Q&A transcript as `.txt`
-  Clear history button
-  Modular code structure (`utils/`)

---

## 🧠 How It Works

1. The user uploads a PDF document.
2. The system loads and extracts text from the file.
3. The text is split into smaller chunks for processing.
4. Embeddings are generated for each chunk.
5. A vector store indexes the embeddings.
6. When the user asks a question, the system retrieves the most relevant chunks.
7. The QA chain generates an answer using the retrieved context.

---

## 🛠 Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core programming language |
| Streamlit | User interface |
| LangChain | QA pipeline |
| ChromaDB | Vector database |
| OpenAI / LLM | Question answering |
| PyPDF | PDF text extraction |

---

## 🗂️ Project Structure

```bash
pdf-qa-assistant/
│
├── app.py
│
├── chroma_db/
│   └── chroma.sqlite3
│
├── utils/
│   ├── pdf_loader.py
│   ├── qa_chain.py
│   └── vector_store.py
│
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/vishmividanege/PDF-Q-A-Assistant.git
cd PDF-Q-A-Assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit app

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

---
