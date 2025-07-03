# app/utils/loader.py
from pathlib import Path

def load_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf_file(file_path: str) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])

def load_documents(folder_path: str) -> list[str]:
    """
    Reads all files in the given folder and returns a list of strings
    """
    all_texts = []
    for path in Path(folder_path).glob("*"):
        if path.suffix == ".txt":
            all_texts.append(load_text_file(str(path)))
        elif path.suffix == ".pdf":
            all_texts.append(load_pdf_file(str(path)))
    return all_texts
