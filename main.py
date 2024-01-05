import streamlit as st
import helpers as helper
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from htmlTemplate import css

def main():
    load_dotenv()

    prompt = None
    
    st.set_page_config(page_title="PDF Analysis App",
                       page_icon=":books:")
    
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    
    st.header("Ask questions about your Document")
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"]{
            position:fixed;
            bottom: 8%;
            padding: 10px;
            z-index: 10;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    
   
    st.subheader("Upload Context PDF(s)")
    uploaded_files = st.file_uploader("Choose a PDF file", type=["pdf"], accept_multiple_files=False)
    if st.button("Submit"):
        with st.spinner("Processing (this may take some time)"): 
            #Parse PDFs
            raw_text = helper.parsePDF(uploaded_files)
            
            chunks = helper.chunker(raw_text)
            st.write(f"Chunk Count: {len(chunks)}")

            #Get VectorStore
            vectorStore = helper.getVectorStore(raw_text, chunks)
            print(vectorStore)

            #Create conversation Chain
            st.session_state.conversation = helper.getConversationChain(vectorStore)

    

    prompt = st.text_input(" ",placeholder="Enter your prompt...", key="prompt")
    if prompt:
        with st.spinner("Processing..."): 
            helper.handelPrompt(prompt)

if __name__ == '__main__':
    main()