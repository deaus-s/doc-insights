"""
rag_engine.py
-------------
Core intelligence layer.
Handles: Q&A, summarization, entity extraction, document comparison.
All powered by Groq Llama 3.3 — free and fast.
"""

from groq import Groq
from langchain_core.documents import Document
from vector_store import retrieve_chunks, retrieve_from_multiple
from dotenv import load_dotenv

load_dotenv()

client = Groq()
MODEL  = "llama-3.3-70b-versatile"


# ── Prompt Templates ─────────────────────────────────────────────────────────

QA_SYSTEM = """You are an expert document analyst assistant.
You answer questions based strictly on the provided document context.

Rules:
- Answer only from the context provided. Never make up information.
- If the answer is not in the context, say: "I could not find this information in the document."
- Always cite the page or section number when possible.
- Be concise but complete. Use bullet points for multi-part answers.
- For legal documents: highlight important clauses or obligations.
- For financial reports: highlight key figures and percentages.
- For research papers: highlight methodology, findings, and limitations.
"""

SUMMARY_SYSTEM = """You are an expert document summarizer.
Create a structured, comprehensive summary of the provided document content.

Format your summary as:
## Overview
(2-3 sentence high-level description)

## Key Points
(5-8 most important bullet points)

## Important Details
(specific figures, dates, names, amounts, obligations, findings)

## Conclusion
(what this document means / what action it implies)
"""

ENTITY_SYSTEM = """You are an expert information extractor.
Extract all important entities from the document context.

Return results in this exact format:

**People & Organizations:**
- (list names, companies, parties)

**Dates & Deadlines:**
- (list all dates and what they refer to)

**Financial Figures:**
- (list all monetary amounts, percentages, financial metrics)

**Key Terms & Clauses:**
- (list important terms, conditions, definitions)

**Locations:**
- (list all places mentioned)

If a category has no items, write "None found."
"""

COMPARE_SYSTEM = """You are an expert document comparison analyst.
You have been given content from two different documents.
Compare them thoroughly based on the user's question.

Format your response as:
## Document 1 — {doc1}
(relevant content from document 1)

## Document 2 — {doc2}
(relevant content from document 2)

## Key Differences
(bullet points of the most important differences)

## Similarities
(bullet points of common themes or matching content)

## Conclusion
(which document is more relevant to the question, and why)
"""


# ── Core Functions ───────────────────────────────────────────────────────────

def format_context(chunks: list[Document]) -> str:
    """Formats retrieved chunks into a clean context string with source citations."""
    parts = []
    for chunk in chunks:
        src  = chunk.metadata.get("source", "Unknown")
        page = chunk.metadata.get("page", "?")
        parts.append(f"[Source: {src}, Page {page}]\n{chunk.page_content}")
    return "\n\n---\n\n".join(parts)


def answer_question(filename: str, question: str, chat_history: list = []) -> dict:
    """
    Main Q&A function.
    Retrieves relevant chunks and generates a grounded answer with citations.
    """
    chunks = retrieve_chunks(filename, question, k=5)

    if not chunks:
        return {
            "answer": "No relevant content found in the document for this question.",
            "sources": [],
            "chunks_used": 0
        }

    context = format_context(chunks)

    # Build conversation history for multi-turn chat
    messages = [{"role": "system", "content": QA_SYSTEM}]
    for turn in chat_history[-4:]:  # last 4 turns for context
        messages.append({"role": "user",      "content": turn["question"]})
        messages.append({"role": "assistant", "content": turn["answer"]})

    messages.append({
        "role": "user",
        "content": f"""Document Context:
{context}

Question: {question}

Answer based strictly on the document context above:"""
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=1024
    )

    answer = response.choices[0].message.content.strip()

    # Build source citations
    sources = []
    seen = set()
    for chunk in chunks:
        key = (chunk.metadata.get("source"), chunk.metadata.get("page"))
        if key not in seen:
            seen.add(key)
            sources.append({
                "file": chunk.metadata.get("source", "Unknown"),
                "page": chunk.metadata.get("page", "?"),
                "preview": chunk.page_content[:120] + "..."
            })

    return {"answer": answer, "sources": sources, "chunks_used": len(chunks)}


def summarize_document(filename: str) -> str:
    """
    Generates a comprehensive structured summary of the entire document.
    Retrieves broad chunks covering different parts of the document.
    """
    # Retrieve many chunks to cover the whole document
    chunks = retrieve_chunks(filename, "document overview summary main points conclusions", k=12)

    if not chunks:
        return "Could not retrieve content from this document."

    context = format_context(chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM},
            {"role": "user",   "content": f"Document: {filename}\n\nContent:\n{context}\n\nGenerate a comprehensive summary:"}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()


def extract_entities(filename: str) -> str:
    """
    Extracts key entities: people, dates, financials, terms, locations.
    Especially useful for legal contracts and financial reports.
    """
    chunks = retrieve_chunks(filename, "names dates amounts parties obligations terms conditions locations", k=10)

    if not chunks:
        return "Could not retrieve content for entity extraction."

    context = format_context(chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": ENTITY_SYSTEM},
            {"role": "user",   "content": f"Document: {filename}\n\nContent:\n{context}\n\nExtract all entities:"}
        ],
        temperature=0.1,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()


def compare_documents(filename1: str, filename2: str, question: str) -> str:
    """
    Compares two documents based on a specific question or topic.
    Retrieves relevant chunks from both and generates a structured comparison.
    """
    chunks = retrieve_from_multiple([filename1, filename2], question, k=5)

    if not chunks:
        return "Could not retrieve content from one or both documents."

    context = format_context(chunks)

    system = COMPARE_SYSTEM.format(doc1=filename1, doc2=filename2)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": f"Context from both documents:\n{context}\n\nQuestion/Topic to compare: {question}"}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()


def generate_questions(filename: str) -> str:
    """
    Auto-generates 8 smart questions the user could ask about this document.
    Useful as a starting point when a user doesn't know what to ask.
    """
    chunks = retrieve_chunks(filename, "main topics themes content overview", k=6)

    if not chunks:
        return ""

    context = format_context(chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a document analysis expert. Generate 8 insightful questions someone might want to ask about this document. Return only a numbered list. No explanations."},
            {"role": "user",   "content": f"Document: {filename}\n\nContent preview:\n{context}\n\nGenerate 8 smart questions:"}
        ],
        temperature=0.7,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()
