"""
rag_engine.py
-------------
Intelligence layer parsing and communicating with Groq Llama 3.3.
"""
from groq import Groq
from langchain_core.documents import Document
from vector_store import retrieve_chunks, retrieve_from_multiple, load_vectorstore
from dotenv import load_dotenv

load_dotenv()
client = Groq()
MODEL = "llama-3.3-70b-versatile"

QA_SYSTEM = """You are an expert document analyst assistant.
Answer the user's prompt using strictly the facts present in the provided document context.

Rules:
- If the answer isn't in the context, say: "I could not find this information in the document."
- Always cite the precise page numbers when available.
- Present structural data points, risks, or timelines as crisp markdown bullets."""

SUMMARY_SYSTEM = """You are an expert document summarizer. Create a structural, comprehensive summary of the text provided.
Format explicitly as follows:
## Overview
(High level description)
## Key Points
(Critical structural bullets)
## Operational Specifics
(Dates, values, compliance factors)"""

def format_context(chunks: list[Document]) -> str:
    parts = []
    for chunk in chunks:
        src = chunk.metadata.get("source", "Unknown")
        page = chunk.metadata.get("page", "?")
        parts.append(f"[Source: {src}, Page {page}]\n{chunk.page_content}")
    return "\n\n---\n\n".join(parts)

def answer_question(filename: str, question: str, chat_history: list = []) -> dict:
    chunks = retrieve_chunks(filename, question, k=6)
    if not chunks:
        return {"answer": "No context found.", "sources": []}
        
    context = format_context(chunks)
    messages = [{"role": "system", "content": QA_SYSTEM}]
    
    for turn in chat_history[-3:]:
        messages.append({"role": "user", "content": turn["question"]})
        messages.append({"role": "assistant", "content": turn["answer"]})
        
    messages.append({
        "role": "user",
        "content": f"Document Context:\n{context}\n\nQuestion: {question}"
    })
    
    response = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.15)
    answer = response.choices[0].message.content.strip()
    
    sources = []
    seen = set()
    for chunk in chunks:
        p = chunk.metadata.get("page", "?")
        if p not in seen:
            seen.add(p)
            sources.append({"page": p})
            
    return {"answer": answer, "sources": sources}

def summarize_document(filename: str) -> str:
    # Upgraded: Pull structured semantic anchors across entire layout bounds
    vs = load_vectorstore(filename)
    all_docs = vs.similarity_search(" ", k=15) # Global semantic surface scrape
    
    context = format_context(all_docs)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM},
            {"role": "user", "content": f"Content to summarize:\n{context}"}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def extract_entities(filename: str) -> str:
    chunks = retrieve_chunks(filename, "signatories corporate identities dates financial metrics liabilities", k=10)
    context = format_context(chunks)
    
    prompt = """Extract all core entities into these exact buckets:
**People & Organizations:**
**Dates & Deadlines:**
**Financial Figures:**
**Key Clauses & Liabilities:**"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Context:\n{context}"}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

def compare_documents(filename1: str, filename2: str, question: str) -> str:
    chunks = retrieve_from_multiple([filename1, filename2], question, k=5)
    context = format_context(chunks)
    
    prompt = f"""Compare {filename1} and {filename2} relative to the query: '{question}'
Format with markdown headings highlighting Key Divergences and Commonalities explicitly."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Combined Context:\n{context}"}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def generate_questions(filename: str) -> str:
    chunks = retrieve_chunks(filename, "core intent executive overview objective summary", k=4)
    context = format_context(chunks)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Generate a numbered list of exactly 5 specific, analytical questions about this text block. No pleasantries."},
            {"role": "user", "content": f"Context:\n{context}"}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()