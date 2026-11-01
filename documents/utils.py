from docx import Document as DocxDocument
from pypdf import PdfReader


def extract_docx(path):

    doc = DocxDocument(path)

    return "\n".join([
        paragraph.text
        for paragraph in doc.paragraphs
    ])



def extract_pdf(path):

    reader = PdfReader(path)

    return "\n".join([
        page.extract_text()
        for page in reader.pages
    ])