import streamlit as st
from parser.parser_jd import parse_jd
from parser.parser_resume import parse_resume
from matcher.matcher import compute_similarity, extract_matched_skills
from scorer.scorer import score_resume
import tempfile
import fitz  # PyMuPDF

st.set_page_config(page_title="InsightHire", layout="centered")
st.title("📄 InsightHire – AI Resume Screener")

st.markdown("Upload resume kamu dan masukkan Job Description untuk melihat tingkat kecocokan.")

#  UPLOAD CV/RESUME
resume_file = st.file_uploader("Upload CV/Resume (.pdf)", type=["pdf"])

# WRITE JOB DESCRIPTION
jd_text = st.text_area("Paste Job Description", height=250)

# Validasi input
if st.button("🔍 Analyze Resume"):
    if not resume_file or not jd_text.strip():
        st.warning("Silakan upload resume dan isi job description.")
    else:
        with st.spinner("🔎 Menganalisis resume..."):
            # Simpan file sementara
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(resume_file.read())
                resume_path = tmp.name

            # Step 1: Parse Resume
            preprocessed_resume = parse_resume(resume_path)
            preprocessed_jd = parse_jd(jd_text)
            st.markdown(preprocessed_resume)
    

          
            result = score_resume(similarity, matched, missing)

            st.success("✅ Analisis selesai!")
            st.subheader("📊 Resume Fit Score:")
            st.progress(min(result['score'] / 100, 1.0))
            st.metric(label="Skor Kecocokan", value=f"{result['score']}%")

            st.subheader("✅ Skill yang Terpenuhi")
            st.write(", ".join(result["matched"]) or "-")

            st.subheader("❌ Skill yang Kurang")
            st.write(", ".join(result["missing"]) or "-")

            st.subheader("💬 Feedback")
            st.info(result["feedback"])
