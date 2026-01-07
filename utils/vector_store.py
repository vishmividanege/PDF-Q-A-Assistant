from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # updated import
import os

# Use a light, fast model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

def create_vector_store(documents, persist_dir="./chroma_db"):
    """
    Create a Chroma vector store from documents and save it in persist_dir.
    """
    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=persist_dir
    )
    return vector_store

def load_vector_store(persist_dir="./chroma_db"):
    """
    Load an existing Chroma vector store from persist_dir.
    Returns None if the directory doesn't exist.
    """
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return None
