from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplate import css, user, sys
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv
import os
import hashlib
import streamlit as st

#Read a pdf into a string
def parsePDF(doc)->str:
    raw_text = ""
    reader = PdfReader(doc)
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

def getConversationChain(vectorStore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorStore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handelPrompt(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(sys.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)



