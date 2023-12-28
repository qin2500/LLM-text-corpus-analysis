from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def parsePDF(docs: list)->str:
    raw_text = ""
    for pdf in docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            raw_text += page.extract_text() 
    return raw_text

def chunker(text: str)->list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = splitter.split_text(text)
    return chunks 


