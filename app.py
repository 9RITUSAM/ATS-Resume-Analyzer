import streamlit as st
from resume_parser import extract_text
from nlp_utils import clean_text, ats_score

st.set_page_config(page_title="ATS Resume Analyzer", layout="centered")
st.title("ATS Resume Analyzer")

uploaded = st.file_uploader("Upload resume (PDF / DOCX / TXT)", type=["pdf","docx","txt"])
jd_text = st.text_area("Paste Job Description (optional)", height=200, placeholder="Paste JD here...")

if st.button("Analyze") and uploaded is not None:
    temp_path = "temp_resume."+uploaded.name.split(".")[-1]
    with open(temp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    txt = clean_text(extract_text(temp_path))
    ats = ats_score(txt, jd_text if jd_text else "", experience_years=1, education_level="bachelors")

    st.subheader("ATS Score")
    st.metric("Total ATS Score", f"{ats['total_score']}%")
    

    st.subheader("Missing Sections")
    st.write(ats["missing_sections"])
    

