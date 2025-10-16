import pdfplumber
import docx

def extract_text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text(path):
    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    if path.lower().endswith((".docx", ".doc")):
        return extract_text_from_docx(path)
    # fallback for plain text
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
