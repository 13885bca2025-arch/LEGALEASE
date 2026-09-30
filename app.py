import html
import os
from datetime import date

import requests
import streamlit as st

from utils.document_formatter import format_docx, format_pdf, format_txt, sanitize_text

BACKEND_URL = os.getenv("LEGALEASE_BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown(
    """
    <style>
    .hero { padding: 1.6rem 2rem; border-radius: 18px; background: linear-gradient(135deg,#111827,#1f2937); color:white; margin-bottom:1.2rem; }
    .hero h1 { margin:0; font-size:2.35rem; }
    .hero p { margin:.45rem 0 0; color:#d1d5db; }
    .card { padding:1rem 1.1rem; border:1px solid rgba(128,128,128,.25); border-radius:14px; }
    .small { font-size:.88rem; opacity:.82; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>⚖️ LegalEase</h1>
      <p>AI-powered legal document drafting, editing, preview, and export.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.0, 1.25], gap="large")

with left:
    st.subheader("1. Document Details")
    document_type = st.text_input(
        "Document Type",
        value="Employment Contract",
        placeholder="e.g. NDA, Lease Agreement, Freelance Work Contract",
    )
    parties = st.text_area(
        "Parties Involved",
        value="ABC Technologies Pvt. Ltd. (Employer); Jane Doe (Employee)",
        height=110,
    )
    terms = st.text_area(
        "Terms & Conditions",
        value="Payment to be made monthly; Confidentiality must be maintained; Either party may terminate with 30 days notice",
        height=160,
        help="Separate clauses with semicolons.",
    )
    effective_date = st.date_input("Effective Date", value=date.today())
    language = st.selectbox("Language", ["English", "Tamil", "Hindi", "Telugu", "Malayalam"])

    if st.button("✨ Generate Document", type="primary", use_container_width=True):
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": effective_date.strftime("%B %d, %Y"),
            "language": language,
        }
        try:
            with st.spinner("Generating your draft..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate", json=payload, timeout=120
                )
            if response.ok:
                data = response.json()
                st.session_state["document"] = data["content"]
                st.session_state["doc_type"] = data["document_type"]
                st.success("Document generated successfully.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(detail or "Backend request failed.")
        except requests.RequestException as exc:
            st.error(f"Could not reach FastAPI backend at {BACKEND_URL}: {exc}")

with right:
    st.subheader("2. Preview & Edit")
    current = st.session_state.get("document", "")
    doc_type = st.session_state.get("doc_type", document_type)

    if current:
        st.markdown(
            f'<div class="card"><div class="small">{html.escape(doc_type)}</div><br>{html.escape(current).replace(chr(10), "<br>")}</div>',
            unsafe_allow_html=True,
        )

        st.divider()
        st.caption("Editable output")
        edited = st.text_area(
            "Edit Document",
            value=current,
            height=430,
            label_visibility="collapsed",
        )
        st.session_state["document"] = edited

        c1, c2, c3 = st.columns(3)
        clean_text = sanitize_text(edited)
        with c1:
            st.download_button(
                "⬇️ TXT",
                data=format_txt(clean_text),
                file_name="legalease_document.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                "⬇️ DOCX",
                data=format_docx(clean_text, doc_type),
                file_name="legalease_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with c3:
            st.download_button(
                "⬇️ PDF",
                data=format_pdf(clean_text, doc_type),
                file_name="legalease_document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.info("Enter the details on the left and click Generate Document.")

st.divider()
st.caption(
    "LegalEase generates editable document drafts. Review the content for your jurisdiction and circumstances before signing or relying on it."
)
