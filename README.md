# 📄 PDF Q&A Assistant (Streamlit)

A simple and clean **PDF Question Answering Assistant** built with **Streamlit**.  
Upload a PDF, process it, and ask questions to get answers based on the document content.  
Includes Q&A history, transcript download, and a UI-focused layout.

---

## ✨ Features
- 📤 Upload a PDF file
- ⚙️ Process PDF (load + split into chunks)
- 🔍 Ask questions about the PDF content
- 🧠 Retrieval-based answering (context + QA chain)
- 🕘 Recent question history (last 10 shown)
- 📥 Download full Q&A transcript as `.txt`
- 🧹 Clear history button
- 🧩 Modular code structure (`utils/`)

---

## 🗂️ Project Structure
```bash
pdf-qa-assistant/
│── app.py
│── utils/
│   ├── pdf_loader.py
│   └── qa_chain.py
│── README.md
