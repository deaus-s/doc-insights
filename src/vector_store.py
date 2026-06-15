"""
vector_store.py
---------------
Manages the ChromaDB vector store.
Each document gets its own collection so they never interfere.
Supports multi-document comparison by querying across collections.
"""

import os
import re
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHROMA_DIR = "data/chroma_db"

# Smart text splitter — 800 char chunks with 150 char overlap
# Overlap ensures context is never lost at chunk boundaries
SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def collection_name(filename: str) -> str:
    """Converts filename to a valid ChromaDB collection name."""
    name = os.path.splitext(filename)[0]
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    name = name[:50]
    if len(name) < 3:
        name = name + "_doc"
    return name.lower()


def index_document(docs: list[Document], filename: str) -> Chroma:
    """
    Splits documents into chunks and indexes them into ChromaDB.
    Each file gets its own collection — clean isolation.
    """
    col_name = collection_name(filename)
    col_path = os.path.join(CHROMA_DIR, col_name)

    # Delete old index for this file if it exists
    if os.path.exists(col_path):
        shutil.rmtree(col_path)

    # Split into smaller overlapping chunks
    chunks = SPLITTER.split_documents(docs)

    # Add chunk index to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = len(chunks)

    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=col_path,
        collection_name=col_name
    )
    return vectorstore


def load_vectorstore(filename: str) -> Chroma:
    """Loads an existing ChromaDB collection for the given filename."""
    col_name = collection_name(filename)
    col_path = os.path.join(CHROMA_DIR, col_name)
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=col_path,
        embedding_function=embeddings,
        collection_name=col_name
    )


def retrieve_chunks(filename: str, query: str, k: int = 5) -> list[Document]:
    """Retrieves top-k most relevant chunks for a query from one document."""
    vs = load_vectorstore(filename)
    return vs.similarity_search(query, k=k)


def retrieve_from_multiple(filenames: list[str], query: str, k: int = 4) -> list[Document]:
    """Retrieves top-k chunks from each document — used for comparison mode."""
    all_chunks = []
    for filename in filenames:
        try:
            chunks = retrieve_chunks(filename, query, k=k)
            all_chunks.extend(chunks)
        except Exception:
            pass
    return all_chunks


def document_exists(filename: str) -> bool:
    """Checks if a document has already been indexed."""
    col_name = collection_name(filename)
    col_path = os.path.join(CHROMA_DIR, col_name)
    return os.path.exists(col_path)


def delete_document(filename: str):
    """Removes a document's index from ChromaDB."""
    col_name = collection_name(filename)
    col_path = os.path.join(CHROMA_DIR, col_name)
    if os.path.exists(col_path):
        shutil.rmtree(col_path)


def list_indexed_documents() -> list[str]:
    """Returns all document collection names currently indexed."""
    if not os.path.exists(CHROMA_DIR):
        return []
    return [d for d in os.listdir(CHROMA_DIR)
            if os.path.isdir(os.path.join(CHROMA_DIR, d))]
