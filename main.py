import streamlit as st
import helpers as helper
from qdrant_client import QdrantClient
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    st.set_page_config(page_title="PDF Analysis App",
                       page_icon=":books:")
    
    st.header("Ask questions about your Document")
    prompt = st.text_area("Enter your prompt:")

    with st.sidebar:
        st.subheader("Upload Context xPDF(s)")
        uploaded_files = st.file_uploader("Choose a PDF file", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit"):
            with st.spinner("Processing (this may take some time)"): 
                #Parse PDFs

                raw_text = helper.parsePDF(uploaded_files)
                
                chunks = helper.chunker(raw_text)
                st.write(f"Chunk Count: {len(chunks)}")

                #Get VectorStore
                vectorStore = helper.getVectorStore(raw_text, chunks)
                print(vectorStore)
                


        st.subheader("Processed PDFs:")

if __name__ == '__main__':
    main()