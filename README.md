<div align="center">

<!-- HEADER BANNER -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=7c3aed&height=200&section=header&text=DocInsights&fontSize=70&fontColor=ffffff&fontAlignY=38&desc=Enterprise%20Document%20Intelligence%20Suite&descAlignY=58&descSize=20&animation=fadeIn" />

<br/>

<!-- BADGES -->
<p>
  <img src="https://img.shields.io/badge/Version-2.5%20PRO-7c3aed?style=for-the-badge&logo=rocket&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.45-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LLaMA-3.3%2070B-0ea5e9?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge" />
</p>

<p>
  <img src="https://img.shields.io/badge/RAG-Hybrid%20Pipeline-f59e0b?style=flat-square&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/VectorDB-ChromaDB-e11d48?style=flat-square&logo=apachekafka&logoColor=white" />
  <img src="https://img.shields.io/badge/Embeddings-Sentence%20Transformers-6366f1?style=flat-square" />
  <img src="https://img.shields.io/badge/Powered%20by-Groq%20API-00D4AA?style=flat-square" />
</p>

<br/>

> **DocInsights** is a production-grade, AI-powered document analysis suite that lets you chat with your documents, extract deep entity maps, generate structured summaries, and run cross-document comparisons — all powered by a Hybrid RAG pipeline with LLaMA 3.3 70B and ChromaDB.

<br/>

</div>

---

## ✦ What is DocInsights?

DocInsights is not just another PDF chatbot. It's a **full-featured document intelligence workstation** designed for professionals who work with contracts, reports, research papers, and datasets. Upload your files, and the system vectorizes them into a semantic search index. Then, ask anything — from specific clause lookups to comparative analysis across multiple documents.

```
Upload → Vectorize → Query → Analyze → Compare
```

---

## ⚡ Core Features

| Feature | Description |
|---|---|
| **💬 Conversational Neural RAG** | Chat with your document using a context-aware Q&A pipeline with page-level citations |
| **📋 Summary Blueprint** | Generate a structured, comprehensive synthesis of any uploaded document |
| **🔍 Deep Entity Map** | Extract key entities, clauses, dates, names, and values with AI-driven parsing |
| **⚖️ Cross-Document Examination** | Compare two documents side-by-side on any criteria — spot differences, conflicts, or shared elements |
| **📥 Multi-Format Ingestion** | Supports **PDF**, **DOCX**, **TXT**, and **CSV** — all vectorized on upload |
| **🎨 Glassmorphic UI** | A luxury dark-mode Streamlit interface with smooth UX, chat bubbles, and real-time feedback |

---

## 🧠 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     DocInsights Suite                       │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  File Upload │───▶│  Doc Parser  │───▶│ Text Chunker  │  │
│  │ PDF/DOCX/TXT│    │  (PyPDF +    │    │  (LangChain   │  │
│  │    /CSV      │    │  python-docx)│    │  Splitter)    │  │
│  └─────────────┘    └──────────────┘    └───────┬───────┘  │
│                                                 │           │
│  ┌──────────────────────────────────────────────▼────────┐  │
│  │              Vector Store (ChromaDB)                  │  │
│  │     Sentence-Transformers Embeddings (Local)          │  │
│  └──────────────────────────────────────────────┬────────┘  │
│                                                 │           │
│  ┌──────────────────────────────────────────────▼────────┐  │
│  │                  RAG Engine                           │  │
│  │   Hybrid Retrieval → Groq API → LLaMA 3.3 70B        │  │
│  │   Q&A / Summary / Entity Extraction / Comparison     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit 1.45 + Custom Glassmorphic CSS |
| **LLM** | LLaMA 3.3 70B via Groq API |
| **RAG Framework** | LangChain (Core + Community + HuggingFace) |
| **Vector Store** | ChromaDB 0.6 |
| **Embeddings** | Sentence-Transformers (local, no API cost) |
| **Document Parsing** | PyPDF, python-docx, pandas |
| **Runtime** | Python 3.10+, PyTorch 2.7 |

</div>

---

## 🧩 Case Studies / Use Cases

Real-world applications built on top of the DocInsights extraction pipeline:

- [Heart Disease Analysis (Power BI)](./heart-disease-powerbi) — DocInsights was used to extract and structure the UCI Heart Disease dataset, which then feeds an interactive Power BI dashboard surfacing the key clinical factors behind CVD diagnosis (exercise-induced angina, chest pain type, major vessel count, and more). [Demo video →](https://youtu.be/QpFf__Gq4xQ)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A [Groq API key](https://console.groq.com/) (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/deaus-s/doc-insights.git
cd doc-insights
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Note:** PyTorch (`torch==2.7.0`) is a large package (~2GB). Install it first if you face issues:
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
> ```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📂 Project Structure

```
doc-insights/
├── app.py                  # Main Streamlit app — UI, layout, session management
├── requirements.txt        # All Python dependencies
├── .env                    # Your API keys (not committed)
├── .gitignore
└── src/
    ├── document_parser.py  # Parses PDF, DOCX, TXT, CSV into LangChain Documents
    ├── vector_store.py     # ChromaDB integration — index, query, delete
    └── rag_engine.py       # Core RAG logic — Q&A, summary, entity extraction, comparison
```

---

## 🔄 How It Works

```
1. UPLOAD   →  Drop any PDF / DOCX / TXT / CSV file
2. INGEST   →  Click "Ingest & Vectorize" — the file is parsed, chunked, and embedded
3. QUERY    →  Type a question in the chat terminal
4. RETRIEVE →  ChromaDB fetches the top-k semantically similar chunks
5. GENERATE →  LLaMA 3.3 70B synthesizes a grounded answer with page citations
6. COMPARE  →  Load two documents and run cross-examination on any criteria
```

---

## 💡 Example Use Cases

- 📑 **Legal Teams** — Compare contracts, flag liability clauses, extract party names and dates
- 🏦 **Finance Analysts** — Summarize annual reports, extract financial figures, compare filings
- 🎓 **Researchers** — Chat with research papers, extract methodology, compare datasets
- 🏗️ **Engineers** — Parse technical specs, identify compliance items, diff two versions of a document
- 🧾 **Business Ops** — Upload invoices/CSVs, extract key data, answer operational queries

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq API key for LLaMA 3.3 70B inference |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by [Shreyash Sonone](https://github.com/deaus-s)**

*NIT Silchar · Electrical Engineering · GenAI & Data Analytics Enthusiast*

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=7c3aed&height=100&section=footer" />

</div>
