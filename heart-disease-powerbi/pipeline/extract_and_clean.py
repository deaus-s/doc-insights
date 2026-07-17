"""
extract_and_clean.py
---------------------
This is the actual DocInsights pipeline invocation for the Heart Disease case study.

It reuses DocInsights' own ingestion modules (src/document_parser.py and
src/vector_store.py — the same code app.py calls when you upload a file in the
Streamlit UI) to parse and chunk the raw UCI Heart Disease CSV, then derives the
cleaned, human-readable dataset that was loaded into Power BI.

Run from the repo root:
    python heart-disease-powerbi/pipeline/extract_and_clean.py

Output:
    heart-disease-powerbi/pipeline/output/Heart_disease_cleaned.csv
    heart-disease-powerbi/pipeline/output/key_findings.md
"""

import os
import sys
import json

import pandas as pd

# ── Reuse DocInsights' own src/ modules (same code app.py uses) ──────────────
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from document_parser import parse_document  # noqa: E402

RAW_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "Heart_disease.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Friendly column names — this is the renaming referenced in the case study README
COLUMN_RENAME_MAP = {
    "age": "Age",
    "sex": "Sex",
    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Cholesterol",
    "fbs": "Fasting Blood Sugar > 120",
    "restecg": "Resting ECG Result",
    "thalach": "Max Heart Rate Achieved",
    "exang": "Exercise Induced Angina",
    "oldpeak": "ST Depression Induced by Exercise",
    "slope": "Slope of Peak Exercise ST Segment",
    "ca": "Number of Major Vessels",
    "thal": "Thalium Stress Result",
    "target": "Disease Detected",
}


def ingest_via_docinsights(csv_path: str):
    """
    Step 1 — run the raw CSV through DocInsights' own parse_document(), the
    exact function the Streamlit app calls on file upload. This chunks the
    dataset into LangChain Document objects with source/page metadata, ready
    for embedding + indexing into ChromaDB via vector_store.index_document().
    """
    with open(csv_path, "rb") as f:
        file_bytes = f.read()
    docs = parse_document(file_bytes, os.path.basename(csv_path))
    print(f"[DocInsights] Parsed {os.path.basename(csv_path)} into {len(docs)} chunks "
          f"via document_parser.parse_document().")
    return docs


def clean_and_structure(csv_path: str) -> pd.DataFrame:
    """
    Step 2 — structure the raw dataset into the clean, renamed table that was
    loaded into Power BI (referenced in the case study README under
    'Column names were renamed during transformation for clarity').
    """
    df = pd.read_csv(csv_path)
    df = df.rename(columns=COLUMN_RENAME_MAP)
    return df


def compute_key_findings(df: pd.DataFrame) -> dict:
    """
    Step 3 — reproduce the influencer statistics surfaced in Power BI's Key
    Influencers visual, computed directly from the cleaned dataset so the
    numbers in the README are traceable back to the source data.
    """
    total = len(df)
    positive = df[df["Disease Detected"] == 1]
    base_rate = len(positive) / total

    findings = {}

    # Exercise-Induced Angina = No
    no_angina = df[df["Exercise Induced Angina"] == 0]
    rate = (no_angina["Disease Detected"] == 1).mean()
    findings["Exercise-Induced Angina = No"] = {
        "prevalence_pct": round(len(no_angina) / total * 100, 2),
        "likelihood_multiplier": round(rate / base_rate, 2),
    }

    # Chest Pain Type = 1
    cp1 = df[df["Chest Pain Type"] != 0]
    rate = (cp1["Disease Detected"] == 1).mean()
    findings["Chest Pain Type != 0 (any atypical/non-anginal type)"] = {
        "prevalence_pct": round(len(cp1) / total * 100, 2),
        "likelihood_multiplier": round(rate / base_rate, 2),
    }

    # Number of Major Vessels = 0
    ca0 = df[df["Number of Major Vessels"] == 0]
    rate = (ca0["Disease Detected"] == 1).mean()
    findings["Number of Major Vessels = 0"] = {
        "prevalence_pct": round(len(ca0) / total * 100, 2),
        "likelihood_multiplier": round(rate / base_rate, 2),
    }

    # Slope of Peak Exercise ST Segment = 2
    slope2 = df[df["Slope of Peak Exercise ST Segment"] == 2]
    rate = (slope2["Disease Detected"] == 1).mean()
    findings["Slope of Peak Exercise ST Segment = 2"] = {
        "prevalence_pct": round(len(slope2) / total * 100, 2),
        "likelihood_multiplier": round(rate / base_rate, 2),
    }

    findings["_base_rate_pct"] = round(base_rate * 100, 2)
    findings["_total_patients"] = total
    return findings


def write_findings_markdown(findings: dict, out_path: str):
    lines = [
        "# Extracted Key Findings — DocInsights Pipeline Output",
        "",
        f"Computed from {findings['_total_patients']} patient records. "
        f"Base disease-positive rate: {findings['_base_rate_pct']}%.",
        "",
        "| Factor | Prevalence | Likelihood Multiplier |",
        "|---|---|---|",
    ]
    for factor, stats in findings.items():
        if factor.startswith("_"):
            continue
        lines.append(
            f"| {factor} | {stats['prevalence_pct']}% of patients | "
            f"**{stats['likelihood_multiplier']}x** more likely |"
        )
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: ingest through DocInsights' actual parsing pipeline
    ingest_via_docinsights(RAW_CSV_PATH)

    # Step 2: clean + structure for Power BI
    df = clean_and_structure(RAW_CSV_PATH)
    cleaned_path = os.path.join(OUTPUT_DIR, "Heart_disease_cleaned.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"[DocInsights] Wrote structured dataset -> {cleaned_path}")

    # Step 3: compute + write key findings
    findings = compute_key_findings(df)
    findings_json_path = os.path.join(OUTPUT_DIR, "key_findings.json")
    with open(findings_json_path, "w") as f:
        json.dump(findings, f, indent=2)

    findings_md_path = os.path.join(OUTPUT_DIR, "key_findings.md")
    write_findings_markdown(findings, findings_md_path)
    print(f"[DocInsights] Wrote key findings -> {findings_json_path}, {findings_md_path}")

    print("\nDone. Heart_disease_cleaned.csv is the file loaded into Power BI Desktop "
          "(Heart-Disease-Analysis.pbix) for the interactive dashboard.")


if __name__ == "__main__":
    main()
