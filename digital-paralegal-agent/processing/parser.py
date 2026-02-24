import io
import pdfplumber
import docx

def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    text_content = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
    return "\n".join(text_content)

def parse_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(io.BytesIO(file_bytes))
    text_content = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(text_content)

def parse_document(file_bytes: bytes, filename: str) -> str:
    """Detect file type and extract text."""
    if filename.lower().endswith('.pdf'):
        return parse_pdf(file_bytes)
    elif filename.lower().endswith('.docx'):
        return parse_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file format for '{filename}'. Only PDF and DOCX are supported.")
