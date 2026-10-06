import io
import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

st.title("Doc Search - Ask My Resume")

openai_api_key = st.sidebar.text_input("Your OpenAI API key", type="password")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

@st.cache_resource(show_spinner="Reading and Indexing your Document...")
def build_vectorstore(file_bytes, api_key):

    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    print(text[:1000])


    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
 
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key = api_key)
    return Chroma.from_texts(texts=chunks, embedding=embeddings,)

if not openai_api_key:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
elif uploaded_file is None:
    st.info("Upload a PDF to get started.")
else:        
    vectorstore = build_vectorstore(uploaded_file.getvalue(), openai_api_key)

    if vectorstore is None:
        st.error("Couldn't read any text from this PDF. It may be a scanned image. Try a PDF with selectable text.")

    else: question = st.text_input("Ask a Question about the Document")

    if question:
        results = vectorstore.similarity_search(question, k=2)
        
        # glue the retrieved chunks into one block of text
        context = ""
        for doc in results:
            context = context + doc.page_content + "\n\n"

        # build the prompt: the facts + the question
        prompt=f"""Use only below information to answer the Question.
    Information:{context}
    Question: {question}
    """

    # ask the chat model
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
        answer = model.invoke(prompt)

        st.write(answer.content)
