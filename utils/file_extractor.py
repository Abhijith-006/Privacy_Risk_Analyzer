import docx
import fitz 

def extract_text_from_file(uploaded_file):
    """
    Extract text from PDF, DOCX, or TXT files.
    """
    if uploaded_file.type=="application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type=="text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return "Unsupported file format !"

def extract_text_from_pdf(file):
    doc=fitz.open(stream=file.read(),filetype="pdf")
    text=""
    for page in doc:
        text+=page.get_text()
    return text

def extract_text_from_docx(file):
    doc=docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])
