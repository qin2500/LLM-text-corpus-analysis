import streamlit as st
import helpers as helper

def main():
    st.set_page_config(page_title="PDF Analysis App",
                       page_icon=":books:")
    
    st.header("Ask questions about your Documents")
    prompt = st.text_area("Enter your prompt:")

    with st.sidebar:
        st.subheader("Upload Context xPDF(s)")
        uploaded_files = st.file_uploader("Choose multiple PDF files", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit"):
            with st.spinner("Processing (they may take some time)"):
                print("poooooooooooooooo")    
                #Parse PDFs
                raw_text = helper.parsePDF(uploaded_files)
                chunks = helper.chunker(raw_text)
                st.write(f"Chunk Count: {len(chunks)}")
                #Generate Vector Stores

        st.subheader("Processed PDFs:")

if __name__ == '__main__':
    main()