from pypdf import PdfReader
from docx import Document
import os


def read_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def read_docx(file_path):
    doc = Document(file_path)

    return "\n".join([para.text for para in doc.paragraphs])


def load_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".pdf"):
            text = read_pdf(file_path)

        elif filename.endswith(".docx"):
            text = read_docx(file_path)

        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            continue

        documents.append({
            "filename": filename,
            "text": text
        })

    return documents