"""
app.py — DocInsights: Smart Document Intelligence
Run with: streamlit run app.py
"""

import sys, os, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DocInsights — Smart Document Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #070710 !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #070710 !important; }
[data-testid="stHeader"], [data-testid="stDecoration"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: #2d2d4e; border-radius: 2px; }

/* NAV */
.di-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 2rem; background: #0a0a14;
    border-bottom: 1px solid #1a1a2e;
}
.di-brand { display: flex; align-items: center; gap: 0.6rem; }
.di-icon {
    width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.di-brand-name { font-size: 1.05rem; font-weight: 700; color: #f1f5f9; }
.di-brand-sub { font-size: 0.72rem; color: #475569; margin-left: 0.3rem; }
.di-badges { display: flex; gap: 0.5rem; }
.di-badge {
    background: #0f0f1e; border: 1px solid #1e1e3e;
    color: #6366f1; font-size: 0.68rem; font-weight: 600;
    padding: 0.2rem 0.6rem; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.05em;
}

/* HERO */
.di-hero { padding: 2.5rem 2rem 1.5rem; }
.di-hero-tag {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.3);
    color: #a78bfa; font-size: 0.7rem; font-weight: 600;
    padding: 0.25rem 0.7rem; border-radius: 20px; margin-bottom: 1rem;
    letter-spacing: 0.06em; text-transform: uppercase;
}
.di-hero h1 {
    font-size: 2.2rem !important; font-weight: 700 !important;
    color: #f8fafc !important; line-height: 1.2 !important;
    margin-bottom: 0.6rem !important;
}
.di-hero h1 span {
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.di-hero p { color: #64748b !important; font-size: 0.95rem !important; }

/* TABS */
[data-testid="stTabs"] { margin-top: 0.5rem; }
[data-testid="stTab"] {
    font-size: 0.82rem !important; font-weight: 500 !important;
    color: #475569 !important; padding: 0.5rem 1rem !important;
}
[aria-selected="true"][data-testid="stTab"] { color: #a78bfa !important; }

/* CARDS */
.di-card {
    background: #0d0d1a; border: 1px solid #1a1a2e;
    border-radius: 12px; padding: 1.4rem;
    margin-bottom: 1rem;
}
.di-card:hover { border-color: #2a2a4e; }
.di-card-title {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.09em;
    text-transform: uppercase; color: #374151; margin-bottom: 0.8rem;
}

/* UPLOAD ZONE */
[data-testid="stFileUploader"] {
    background: #0d0d1a !important;
    border: 1.5px dashed #2d2d4e !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #8b5cf6 !important; }

/* DOC LIST */
.di-doc-item {
    display: flex; align-items: center; gap: 0.6rem;
    background: #0f0f1e; border: 1px solid #1a1a2e;
    border-radius: 8px; padding: 0.6rem 0.8rem;
    margin-bottom: 0.4rem; cursor: pointer;
    transition: all 0.15s;
}
.di-doc-item:hover { border-color: #8b5cf6; }
.di-doc-item.active { border-color: #8b5cf6; background: rgba(139,92,246,0.08); }
.di-doc-icon { font-size: 1rem; }
.di-doc-name { font-size: 0.8rem; color: #94a3b8; flex: 1; }
.di-doc-type { font-size: 0.65rem; color: #374151; font-family: 'JetBrains Mono', monospace; }

/* CHAT */
.di-msg-user {
    background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2);
    border-radius: 10px 10px 4px 10px; padding: 0.8rem 1rem;
    margin-bottom: 0.6rem; margin-left: 2rem;
    font-size: 0.9rem; color: #c4b5fd;
}
.di-msg-ai {
    background: #0d0d1a; border: 1px solid #1a1a2e;
    border-radius: 10px 10px 10px 4px; padding: 1rem 1.2rem;
    margin-bottom: 1rem; font-size: 0.88rem;
    color: #cbd5e1; line-height: 1.7;
}
.di-source-chip {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: #0f0f1e; border: 1px solid #1e1e3e;
    color: #6366f1; font-size: 0.68rem;
    padding: 0.15rem 0.5rem; border-radius: 4px;
    font-family: 'JetBrains Mono', monospace; margin: 0.2rem 0.2rem 0 0;
}

/* INPUT */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background: #0d0d1a !important;
    border: 1.5px solid #1a1a2e !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #2d2d4e !important; }

/* BUTTONS */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.88rem !important;
}
[data-testid="stButton"] > button:not([kind="primary"]) {
    background: #0d0d1a !important; color: #64748b !important;
    border: 1px solid #1a1a2e !important; border-radius: 6px !important;
    font-size: 0.78rem !important;
}
[data-testid="stButton"] > button:not([kind="primary"]):hover {
    border-color: #8b5cf6 !important; color: #a78bfa !important;
}

/* SELECT */
[data-testid="stSelectbox"] > div > div {
    background: #0d0d1a !important;
    border: 1.5px solid #1a1a2e !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* DIVIDER */
hr { border-color: #1a1a2e !important; margin: 1rem 0 !important; }

/* SUMMARY / ENTITY output */
.di-output {
    background: #080810; border: 1px solid #1a1a2e; border-radius: 10px;
    padding: 1.2rem 1.4rem; font-size: 0.88rem; color: #cbd5e1;
    line-height: 1.8; white-space: pre-wrap;
}

/* STATUS */
.di-status { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; color: #475569; }
.di-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; animation: blink 2s infinite; }
.di-dot-orange { background: #f59e0b; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* EMPTY */
.di-empty { text-align: center; padding: 3rem; color: #1e1e3e; }
.di-empty-icon { font-size: 3rem; opacity: 0.2; margin-bottom: 0.8rem; }
.di-empty-text { font-size: 0.88rem; color: #2d2d4e; }

/* PROGRESS */
[data-testid="stProgress"] > div > div { background: #8b5cf6 !important; }
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
defaults = {
    "documents": {},        # {filename: {"path": ..., "pages": ..., "size": ...}}
    "active_doc": None,
    "compare_doc": None,
    "chat_history": {},     # {filename: [{"question":..., "answer":..., "sources":...}]}
    "suggested_qs": {},     # {filename: [list of questions]}
    "tab": "chat",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="di-nav">
    <div class="di-brand">
        <div class="di-icon">◈</div>
        <span class="di-brand-name">DocInsights</span>
        <span class="di-brand-sub">Smart Document Intelligence</span>
    </div>
    <div class="di-badges">
        <span class="di-badge">RAG</span>
        <span class="di-badge">ChromaDB</span>
        <span class="di-badge">Groq LLM</span>
        <span class="di-badge">HuggingFace</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="di-hero">
    <div class="di-hero-tag">◈ AI-Powered Document Analysis</div>
    <h1>Understand any document,<br><span>instantly.</span></h1>
    <p>Upload legal contracts, research papers, financial reports, or any document.
    Ask questions, get summaries, extract entities, compare documents — all with AI.</p>
</div>
""", unsafe_allow_html=True)


# ── LAYOUT ────────────────────────────────────────────────────────────────────
sidebar_col, main_col = st.columns([1, 2.8], gap="small")


# ════════════════════════════════════════
# SIDEBAR — Upload + Document List
# ════════════════════════════════════════
with sidebar_col:

    # Upload
    st.markdown('<div class="di-card-title">Upload Documents</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        from document_parser import parse_document
        from vector_store import index_document, document_exists

        for uf in uploaded_files:
            if uf.name not in st.session_state.documents:
                with st.spinner(f"Indexing {uf.name}..."):
                    file_bytes = uf.read()
                    docs = parse_document(file_bytes, uf.name)
                    index_document(docs, uf.name)
                    st.session_state.documents[uf.name] = {
                        "pages": len(docs),
                        "size": f"{len(file_bytes) / 1024:.1f} KB",
                        "type": uf.name.split(".")[-1].upper()
                    }
                    if uf.name not in st.session_state.chat_history:
                        st.session_state.chat_history[uf.name] = []
                    st.session_state.active_doc = uf.name
                st.success(f"✓ {uf.name} indexed")

    st.divider()

    # Document list
    if st.session_state.documents:
        st.markdown('<div class="di-card-title">Your Documents</div>', unsafe_allow_html=True)

        type_icons = {"PDF": "📄", "DOCX": "📝", "TXT": "📃", "CSV": "📊"}

        for fname, meta in st.session_state.documents.items():
            is_active = fname == st.session_state.active_doc
            icon = type_icons.get(meta["type"], "📄")
            css  = "di-doc-item active" if is_active else "di-doc-item"

            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(
                    f"{icon} {fname[:28]}{'…' if len(fname) > 28 else ''}",
                    key=f"doc_{fname}",
                    use_container_width=True
                ):
                    st.session_state.active_doc = fname
                    st.rerun()
            with col2:
                if st.button("✕", key=f"del_{fname}"):
                    from vector_store import delete_document
                    delete_document(fname)
                    del st.session_state.documents[fname]
                    if fname in st.session_state.chat_history:
                        del st.session_state.chat_history[fname]
                    if st.session_state.active_doc == fname:
                        remaining = list(st.session_state.documents.keys())
                        st.session_state.active_doc = remaining[0] if remaining else None
                    st.rerun()

            if is_active:
                st.caption(f"{meta['pages']} sections · {meta['size']} · {meta['type']}")

        st.divider()

        # Compare mode
        if len(st.session_state.documents) >= 2:
            st.markdown('<div class="di-card-title">Compare Mode</div>', unsafe_allow_html=True)
            doc_names = list(st.session_state.documents.keys())
            st.session_state.compare_doc = st.selectbox(
                "Compare active doc with:",
                [d for d in doc_names if d != st.session_state.active_doc],
                key="compare_select",
                label_visibility="collapsed"
            )
    else:
        st.markdown("""
        <div class="di-empty">
            <div class="di-empty-icon">◈</div>
            <div class="di-empty-text">Upload a document above to get started</div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════
# MAIN PANEL
# ════════════════════════════════════════
with main_col:

    if not st.session_state.active_doc:
        st.markdown("""
        <div class="di-empty" style="padding:5rem">
            <div class="di-empty-icon">◈</div>
            <div class="di-empty-text">Upload a document on the left to begin analysis</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        active = st.session_state.active_doc
        meta   = st.session_state.documents[active]

        # Active doc header
        type_icons = {"PDF": "📄", "DOCX": "📝", "TXT": "📃", "CSV": "📊"}
        st.markdown(f"""
        <div class="di-status">
            <div class="di-dot"></div>
            <strong style="color:#94a3b8">{active}</strong>
            <span style="color:#374151">·</span>
            <span>{meta['pages']} sections</span>
            <span style="color:#374151">·</span>
            <span>{meta['size']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(" ")

        # ── TABS ─────────────────────────────────────────────────────────────
        tab_chat, tab_summary, tab_entities, tab_compare = st.tabs([
            "💬 Chat", "📋 Summary", "🔍 Extract Entities", "⚖️ Compare"
        ])

        # ════════════════
        # TAB 1: CHAT
        # ════════════════
        with tab_chat:
            history = st.session_state.chat_history.get(active, [])

            # Suggested questions
            if not history:
                if active not in st.session_state.suggested_qs:
                    from rag_engine import generate_questions
                    with st.spinner("Generating suggested questions..."):
                        raw = generate_questions(active)
                        qs  = [q.strip() for q in raw.split("\n") if q.strip() and q[0].isdigit()]
                        qs  = [q.split(". ", 1)[-1] if ". " in q else q for q in qs]
                        st.session_state.suggested_qs[active] = qs[:8]

                suggested = st.session_state.suggested_qs.get(active, [])
                if suggested:
                    st.markdown('<div class="di-card-title">Suggested Questions</div>', unsafe_allow_html=True)
                    cols = st.columns(2)
                    for i, q in enumerate(suggested):
                        if cols[i % 2].button(q, key=f"sq_{i}_{active}"):
                            st.session_state["prefill_q"] = q
                            st.rerun()

            # Chat history display
            for turn in history:
                st.markdown(f'<div class="di-msg-user">🧑 {turn["question"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="di-msg-ai">{turn["answer"]}</div>', unsafe_allow_html=True)
                if turn.get("sources"):
                    for src in turn["sources"]:
                        st.markdown(
                            f'<span class="di-source-chip">📄 Page {src["page"]}</span>',
                            unsafe_allow_html=True
                        )
                st.markdown(" ")

            # Input
            prefill = st.session_state.pop("prefill_q", "")
            question = st.text_input(
                "Ask a question",
                value=prefill,
                placeholder="e.g. What are the key obligations in this contract?",
                key=f"chat_input_{active}",
                label_visibility="collapsed"
            )

            c1, c2, c3 = st.columns([1, 4, 1])
            with c1:
                ask_btn = st.button("◈ Ask", type="primary", key="ask_btn")
            with c3:
                if st.button("Clear chat", key="clear_chat"):
                    st.session_state.chat_history[active] = []
                    if active in st.session_state.suggested_qs:
                        del st.session_state.suggested_qs[active]
                    st.rerun()

            if ask_btn and question.strip():
                from rag_engine import answer_question
                with st.spinner("Analysing document..."):
                    result = answer_question(
                        active,
                        question.strip(),
                        chat_history=history
                    )
                st.session_state.chat_history[active].append({
                    "question": question.strip(),
                    "answer":   result["answer"],
                    "sources":  result["sources"]
                })
                st.rerun()

        # ════════════════
        # TAB 2: SUMMARY
        # ════════════════
        with tab_summary:
            st.markdown("Generate a comprehensive structured summary of the entire document.")
            st.markdown(" ")

            if st.button("◈ Generate Summary", type="primary", key="gen_summary"):
                from rag_engine import summarize_document
                with st.spinner("Reading and summarising the document..."):
                    summary = summarize_document(active)
                st.session_state[f"summary_{active}"] = summary

            if f"summary_{active}" in st.session_state:
                st.markdown(
                    st.session_state[f"summary_{active}"]
                )

        # ════════════════
        # TAB 3: ENTITIES
        # ════════════════
        with tab_entities:
            st.markdown("Extract key entities: people, dates, financial figures, terms, and locations.")
            st.markdown(" ")

            if st.button("◈ Extract Entities", type="primary", key="gen_entities"):
                from rag_engine import extract_entities
                with st.spinner("Extracting entities from document..."):
                    entities = extract_entities(active)
                st.session_state[f"entities_{active}"] = entities

            if f"entities_{active}" in st.session_state:
                st.markdown(st.session_state[f"entities_{active}"])

        # ════════════════
        # TAB 4: COMPARE
        # ════════════════
        with tab_compare:
            if len(st.session_state.documents) < 2:
                st.info("Upload at least 2 documents to use comparison mode.")
            else:
                compare_doc = st.session_state.get("compare_doc")
                st.markdown(f"Comparing **{active}** with **{compare_doc}**")
                st.markdown(" ")

                compare_q = st.text_input(
                    "What do you want to compare?",
                    placeholder="e.g. Compare the payment terms and obligations",
                    key="compare_input",
                    label_visibility="collapsed"
                )

                if st.button("◈ Compare Documents", type="primary", key="compare_btn"):
                    if compare_q.strip() and compare_doc:
                        from rag_engine import compare_documents
                        with st.spinner("Comparing documents..."):
                            comparison = compare_documents(active, compare_doc, compare_q.strip())
                        st.session_state["comparison_result"] = comparison

                if "comparison_result" in st.session_state:
                    st.markdown(st.session_state["comparison_result"])
