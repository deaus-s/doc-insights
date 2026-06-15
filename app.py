"""
app.py — DocInsights: Enterprise Document Intelligence Suite
Run with: streamlit run app.py
"""

import sys, os, tempfile, shutil
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_IMPL"] = "None"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DocInsights Suite",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── ADVANCED GLASSMORPHIC STYLING ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Reset and Global Overrides */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #030307 !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #030307 !important; }
[data-testid="stHeader"], [data-testid="stDecoration"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #06060c; }
::-webkit-scrollbar-thumb { background: #1e1e38; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #2a2a50; }

/* Top Luxury Navigation Bar */
.di-navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.85rem 2.5rem; background: rgba(6, 6, 14, 0.85);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    position: sticky; top: 0; z-index: 999;
}
.di-nav-logo-group { display: flex; align-items: center; gap: 0.75rem; }
.di-nav-icon {
    width: 32px; height: 32px; border-radius: 10px;
    background: linear-gradient(135deg, #7c3aed, #0ea5e9);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem; font-weight: bold; color: #fff;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}
.di-nav-title { font-size: 1.2rem; font-weight: 800; letter-spacing: -0.02em; color: #ffffff; }
.di-nav-version {
    font-size: 0.68rem; font-weight: 600; color: #3b82f6; 
    background: rgba(59, 130, 246, 0.1); padding: 0.1rem 0.4rem; 
    border-radius: 6px; border: 1px solid rgba(59, 130, 246, 0.15);
}
.di-nav-badges { display: flex; gap: 0.6rem; align-items: center; }
.di-nav-badge {
    background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05);
    color: #94a3b8; font-size: 0.72rem; font-weight: 600;
    padding: 0.25rem 0.7rem; border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
}

.section-headline {
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #64748b; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
}

/* Document Repository Cards Custom Button Wrappers */
div.stButton > button.repo-btn-active {
    background: linear-gradient(90deg, rgba(124, 58, 237, 0.15) 0%, rgba(14, 165, 233, 0.04) 100%) !important;
    border: 1px solid #7c3aed !important;
    color: #ffffff !important;
    text-align: left !important;
    padding: 0.75rem 1rem !important;
    border-radius: 12px !important;
    display: block !important;
    width: 100% !important;
}
div.stButton > button.repo-btn-inactive {
    background: rgba(255, 255, 255, 0.01) !important;
    border: 1px solid rgba(255, 255, 255, 0.04) !important;
    color: #94a3b8 !important;
    text-align: left !important;
    padding: 0.75rem 1rem !important;
    border-radius: 12px !important;
    display: block !important;
    width: 100% !important;
}
div.stButton > button.repo-btn-inactive:hover {
    border-color: rgba(124, 58, 237, 0.4) !important;
    background: rgba(124, 58, 237, 0.02) !important;
    color: #ffffff !important;
}

/* File Uploader Customizations */
[data-testid="stFileUploader"] {
    background: rgba(9, 9, 20, 0.6) !important;
    border: 1.5px dashed rgba(124, 58, 237, 0.25) !important;
    border-radius: 14px !important; padding: 0.5rem !important;
}

/* Chat Stream Components */
.bubble-user {
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(124, 58, 237, 0.05));
    border: 1px solid rgba(124, 58, 237, 0.25);
    border-radius: 14px 14px 4px 14px; padding: 1rem 1.25rem;
    margin-bottom: 0.75rem; font-size: 0.92rem; color: #e9d5ff;
    line-height: 1.6; max-width: 85%; margin-left: auto;
}
.bubble-ai {
    background: rgba(15, 15, 32, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 14px 14px 14px 4px; padding: 1.25rem 1.5rem;
    margin-bottom: 0.5rem; font-size: 0.94rem; color: #e2e8f0;
    line-height: 1.7; max-width: 90%;
    backdrop-filter: blur(5px);
}
.source-chip-tray { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1.5rem; padding-left: 0.2rem; }
.source-page-chip {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: rgba(14, 165, 233, 0.06); border: 1px solid rgba(14, 165, 233, 0.2);
    color: #38bdf8; font-size: 0.7rem; font-weight: 600;
    padding: 0.2rem 0.6rem; border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
}

/* Studio Workstation Framework Layout */
.studio-container { padding: 2rem 2.5rem; }
.studio-output-slate {
    background: rgba(7, 7, 15, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 14px; padding: 1.5rem;
    font-size: 0.94rem; color: #cbd5e1; line-height: 1.8;
    margin-top: 1.2rem;
}

.pulse-container { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; font-weight: 600; color: #10b981; }
.pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981; animation: pulseBlink 2s infinite; }
@keyframes pulseBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

/* Universal Inputs */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background: rgba(9, 9, 20, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important; color: #f8fafc !important;
    font-size: 0.92rem !important; padding: 0.75rem 1rem !important;
}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
    border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}

/* Action Button Overrides */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.6rem 1.4rem !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}
[data-testid="stButton"] > button[kind="primary"]:hover { transform: translateY(-1px); }

.workspace-empty-state { text-align: center; padding: 3.5rem 2rem; border: 1px dashed rgba(255, 255, 255, 0.03); border-radius: 14px; }
.workspace-empty-icon { font-size: 2.2rem; margin-bottom: 0.75rem; color: #7c3aed; }
.workspace-empty-text { font-size: 0.88rem; color: #475569; }
</style>
""", unsafe_allow_html=True)

# ── INSTANT SYSTEM SESSION STATE ARCHITECTURE ─────────────────────────────────
defaults = {
    "documents": {},
    "active_doc": None,
    "compare_doc": None,
    "chat_history": {},
    "suggested_qs": {},
    "comparison_results": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── PERSISTENT SYSTEM NAVBAR ──────────────────────────────────────────────────
st.markdown("""
<div class="di-navbar">
    <div class="di-nav-logo-group">
        <div class="di-nav-icon">◈</div>
        <span class="di-nav-title">DocInsights</span>
        <span class="di-nav-version">v2.5 PRO</span>
    </div>
    <div class="di-nav-badges">
        <span class="di-nav-badge">Hybrid RAG</span>
        <span class="di-nav-badge">Llama 3.3 70B</span>
        <span class="di-nav-badge">ChromaDB</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="studio-container">', unsafe_allow_html=True)
left_pane, right_pane = st.columns([1, 2.6], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT PANE: CONTROLS & REPOSITORY INGESTION
# ══════════════════════════════════════════════════════════════════════════════
with left_pane:
    st.markdown('<div class="section-headline">📥 File Ingestion</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload Hub",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        from document_parser import parse_document
        from vector_store import index_document

        for uf in uploaded_files:
            if uf.name not in st.session_state.documents:
                with st.spinner(f"Vectorizing {uf.name}..."):
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
                st.toast(f"✓ Indexed {uf.name}")
        st.rerun()

    st.markdown('<div style="margin-top:2rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-headline">📂 Active Repository</div>', unsafe_allow_html=True)

    if st.session_state.documents:
        type_icons = {"PDF": "📄", "DOCX": "📝", "TXT": "📃", "CSV": "📊"}

        for fname, meta in list(st.session_state.documents.items()):
            is_active = (fname == st.session_state.active_doc)
            icon = type_icons.get(meta["type"], "📄")
            btn_style = "repo-btn-active" if is_active else "repo-btn-inactive"
            
            card_col, del_col = st.columns([5, 1])
            with card_col:
                # FIXED: Unified interactive selection frame to prevent broken state tracking loop
                if st.button(
                    f"{icon} {fname[:22]}... ({meta['type']})", 
                    key=f"card_select_{fname}", 
                    class_name=btn_style, 
                    use_container_width=True
                ):
                    st.session_state.active_doc = fname
                    st.rerun()
            with del_col:
                if st.button("✕", key=f"drop_{fname}", use_container_width=True):
                    from vector_store import delete_document
                    try:
                        delete_document(fname)
                    except:
                        pass
                    del st.session_state.documents[fname]
                    if fname in st.session_state.chat_history:
                        del st.session_state.chat_history[fname]
                    if st.session_state.active_doc == fname:
                        remaining = list(st.session_state.documents.keys())
                        st.session_state.active_doc = remaining[0] if remaining else None
                    st.rerun()
                    
        if len(st.session_state.documents) >= 2:
            st.markdown('<div style="margin-top:2.5rem"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-headline">⚖️ Comparative Context Target</div>', unsafe_allow_html=True)
            doc_names = list(st.session_state.documents.keys())
            cross_options = [d for d in doc_names if d != st.session_state.active_doc]
            st.session_state.compare_doc = st.selectbox(
                "Target Select", cross_options, key="studio_compare_select", label_visibility="collapsed"
            )
    else:
        st.markdown("""
        <div class="workspace-empty-state">
            <div class="workspace-empty-icon">◈</div>
            <div class="workspace-empty-text">Storage pipeline empty. Upload files above to begin.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANE: ANALYTICAL ENGINE WORKBENCH
# ══════════════════════════════════════════════════════════════════════════════
with right_pane:
    if not st.session_state.active_doc:
        st.markdown("""
        <div style="background:rgba(10,10,22,0.3); border:1px dashed rgba(255,255,255,0.04); border-radius:24px; padding:8rem 2rem; text-align:center; margin-top:1rem;">
            <div style="font-size:4rem; margin-bottom:1.5rem; background:linear-gradient(135deg, #7c3aed, #0ea5e9); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:bold;">◈</div>
            <h2 style="font-weight:700; color:#ffffff; font-size:1.4rem;">DocInsights Engine Awaiting Target</h2>
            <p style="color:#475569; max-width:440px; margin:0.5rem auto 0; font-size:0.92rem; line-height:1.6;">Select a source framework from your active repository list on the left to mount the context terminal.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        active = st.session_state.active_doc
        meta = st.session_state.documents[active]

        st.markdown(f"""
        <div style="border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:1.2rem; margin-bottom:1.5rem;">
            <div class="pulse-container"><div class="pulse-dot"></div>CONTEXT FRAME ACTIVE ({meta['type']})</div>
            <h2 style="font-size:1.4rem; font-weight:800; color:#ffffff; margin-top:0.2rem; letter-spacing:-0.02em;">{active}</h2>
        </div>
        """, unsafe_allow_html=True)

        engine_tab_chat, engine_tab_summary, engine_tab_entities, engine_tab_compare = st.tabs([
            "💬 Conversational Neural RAG", "📋 Summary Blueprint", "🔍 Deep Entity Map", "⚖️ Cross Examination"
        ])

        # 🚀 WORKSTATION TAB 1: CONVERSATIONAL NEURAL RAG
        with engine_tab_chat:
            chat_stream = st.session_state.chat_history.get(active, [])

            if not chat_stream:
                if active not in st.session_state.suggested_qs:
                    from rag_engine import generate_questions
                    with st.spinner("Compiling structural analytical prompts..."):
                        try:
                            raw_prompts = generate_questions(active)
                            parsed_qs = [q.strip() for q in raw_prompts.split("\n") if q.strip() and (q[0].isdigit() or q.startswith("-"))]
                            parsed_qs = [q.split(". ", 1)[-1] if ". " in q else q for q in parsed_qs]
                            st.session_state.suggested_qs[active] = [q.lstrip("- ").strip() for q in parsed_qs][:4]
                        except:
                            st.session_state.suggested_qs[active] = ["Summarize key requirements", "Identify liability limits"]

                suggested_prompts = st.session_state.suggested_qs.get(active, [])
                if suggested_prompts:
                    st.markdown('<div class="section-headline" style="margin-top:0.5rem;">💡 Suggested Explorations</div>', unsafe_allow_html=True)
                    col_q1, col_q2 = st.columns(2, gap="small")
                    for idx, question_str in enumerate(suggested_prompts):
                        target_col = col_q1 if idx % 2 == 0 else col_q2
                        if target_col.button(f"→ {question_str}", key=f"studio_sq_{idx}_{active}", use_container_width=True):
                            st.session_state["prefill_q"] = question_str
                            st.rerun()
                    st.markdown('<hr style="opacity:0.3; margin:1.5rem 0;" />', unsafe_allow_html=True)

            for message_turn in chat_stream:
                st.markdown(f'<div class="bubble-user"><b>User</b><br>{message_turn["question"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bubble-ai"><b>DocInsights Intelligence Suite</b><br><br>{message_turn["answer"]}</div>', unsafe_allow_html=True)
                if message_turn.get("sources"):
                    chips_markup = '<div class="source-chip-tray">'
                    for source_meta in message_turn["sources"]:
                        chips_markup += f'<span class="source-page-chip">📍 Citation: Page {source_meta["page"]}</span>'
                    chips_markup += '</div>'
                    st.markdown(chips_markup, unsafe_allow_html=True)

            prefill_val = st.session_state.pop("prefill_q", "")
            user_prompt = st.text_input(
                "Prompt Input Terminal",
                value=prefill_val,
                placeholder="Ask specific questions regarding this document context...",
                key=f"studio_input_bind_{active}",
                label_visibility="collapsed"
            )

            deck_btn1, deck_spacer, deck_btn2 = st.columns([1.2, 3, 1.2])
            with deck_btn1:
                # SUBMIT ACTION IS VISIBLE HERE NOW
                execute_query = st.button("◈ Execute Prompt", type="primary", key=f"studio_run_prompt_{active}", use_container_width=True)
            with deck_btn2:
                if st.button("Flush History", key=f"studio_flush_{active}", use_container_width=True):
                    st.session_state.chat_history[active] = []
                    st.rerun()

            if execute_query and user_prompt.strip():
                from rag_engine import answer_question
                with st.spinner("Querying local context planes..."):
                    query_payload = answer_question(active, user_prompt.strip(), chat_history=chat_stream)
                st.session_state.chat_history[active].append({
                    "question": user_prompt.strip(),
                    "answer": query_payload["answer"],
                    "sources": query_payload["sources"]
                })
                st.rerun()

        # 📋 WORKSTATION TAB 2: SUMMARY COMPILATION
        with engine_tab_summary:
            if st.button("◈ Run Document Synthesis", type="primary", key=f"studio_sum_exec_{active}"):
                from rag_engine import summarize_document
                with st.spinner("Synthesizing context fields..."):
                    compiled_summary = summarize_document(active)
                st.session_state[f"summary_workspace_{active}"] = compiled_summary

            if f"summary_workspace_{active}" in st.session_state:
                st.markdown(f'<div class="studio-output-slate">{st.session_state[f"summary_workspace_{active}"]}</div>', unsafe_allow_html=True)

        # 🔍 WORKSTATION TAB 3: DEEP ENTITY EXTRACTION
        with engine_tab_entities:
            if st.button("◈ Extract Entity Frameworks", type="primary", key=f"studio_ent_exec_{active}"):
                from rag_engine import extract_entities
                with st.spinner("Running high-dimensional parsing models..."):
                    extracted_payload = extract_entities(active)
                st.session_state[f"entities_workspace_{active}"] = extracted_payload

            if f"entities_workspace_{active}" in st.session_state:
                st.markdown(f'<div class="studio-output-slate">{st.session_state[f"entities_workspace_{active}"]}</div>', unsafe_allow_html=True)

        # ⚖️ WORKSTATION TAB 4: CROSS-DOCUMENT EXAMINATION
        with engine_tab_compare:
            target_cross_name = st.session_state.get("compare_doc")
            if not target_cross_name:
                st.info("Ingest multiple source materials within the local system to deploy concurrent comparison matrix arrays.")
            else:
                st.markdown(f"<div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04); padding:0.8rem 1.2rem; border-radius:10px; font-size:0.9rem; color:#94a3b8;'>Cross Examination: Base <b>{active}</b> ⟷ Target <b>{target_cross_name}</b></div>", unsafe_allow_html=True)
                st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
                
                cross_criteria_prompt = st.text_input(
                    "Comparison Query Parameters",
                    placeholder="Identify variances in liability ceilings, timelines, or compliance values...",
                    key=f"studio_cross_input_{active}",
                    label_visibility="collapsed"
                )

                if st.button("◈ Execute Comparison Matrix", type="primary", key=f"studio_cross_exec_{active}"):
                    if cross_criteria_prompt.strip():
                        from rag_engine import compare_documents
                        with st.spinner("Mapping intersections across token spaces..."):
                            cross_output = compare_documents(active, target_cross_name, cross_criteria_prompt.strip())
                        pair_isolated_hash = f"{active}_vs_{target_cross_name}"
                        st.session_state["comparison_results"][pair_isolated_hash] = cross_output

                pair_isolated_hash = f"{active}_vs_{target_cross_name}"
                if pair_isolated_hash in st.session_state["comparison_results"]:
                    st.markdown(f'<div class="studio-output-slate">{st.session_state["comparison_results"][pair_isolated_hash]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)