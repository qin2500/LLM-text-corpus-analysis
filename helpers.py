from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv
import os
import hashlib
import streamlit as st

#Read a pdf into a string
def parsePDF(docs: list)->str:
    raw_text = ""
    for pdf in docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            raw_text += page.extract_text() 
    return raw_text

#Split string into chunks using langchain
def chunker(text: str)->list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = splitter.split_text(text)
    return chunks 

def getHash(text: str):
    truncated_string = text[:500] + text[-500:]   
    sha256_hash = hashlib.sha256()    
    sha256_hash.update(truncated_string.encode('utf-8'))
    hash_code = sha256_hash.hexdigest()
    
    return hash_code
    

def getVectorStore(text: str, chunks:list):
    load_dotenv()

    #Connect to qdrant database
    qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_HOST"), 
    api_key=os.getenv("QDRANT_API_KEY")
    )

    #Get hash code for inputed pdf
    PDFhash = getHash(text)

    found = False

    try:
        #See if collection with name {hash} alsoready exists
        info = qdrant_client.get_collection(collection_name=PDFhash)
        st.write(info)

        if info.vectors_count != 0: 
            found = True

    except UnexpectedResponse as e: 
        #TODO: Right now, this catches ALL error codes. Should make cases for different error codes.
        #Create qdrant collection
        print(e)
        qdrant_client.create_collection(
        collection_name=f"{PDFhash}",
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    #Generate and store vector embedding of pdf
    embedding = OpenAIEmbeddings()
    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=PDFhash,
        embeddings=embedding
    )

    if not found:
        st.write("Spending money")
        vector_store.add_texts(chunks)
    else:
        st.write("Saving money")

    return vector_store





