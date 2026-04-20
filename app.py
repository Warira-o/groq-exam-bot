import streamlit as st
import os
from dotnev import load_dotnev
load_dotnev()
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- NEW LANGCHAIN IMPORTS ---
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Setup Page & Credentials
st.set_page_config(page_title="Groq Exam Prep", layout="wide")
st.title("⚡ Groq-Powered Exam Bot")



# 2. File Upload Sidebar
with st.sidebar:
    st.header("Upload Materials")
    uploaded_file = st.file_uploader("Upload Study PDF", type="pdf")
    process_btn = st.button("Process PDF")

# 3. RAG Logic
if uploaded_file and process_btn:
    with st.spinner("Analyzing your textbook..."):
        # Save temp file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())

        # Load and Chunk
        loader = PyPDFLoader("temp.pdf")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        # Create Embeddings (Free, runs locally)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        # Save vectorstore to session state so it persists
        st.session_state.vectorstore = vectorstore
        st.success("Ready for questions!")

# 4. Chat Interface
if "vectorstore" in st.session_state:
    
    # --- UPDATED PROMPT & CHAIN SETUP ---
    system_prompt = """
    You are a strict but helpful Exam Tutor. Use the following pieces of context to answer the student's question.
    If they ask for a question, generate a Multiple Choice Question (MCQ) based on the text.
    If they answer, tell them if they are right and explain why using the text.
    
    Context:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    # Setup LLM
    llm = ChatGroq(model_name="llama-3.1-70b-versatile", temperature=0.3)
    
    # Create the modern Retrieval Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(st.session_state.vectorstore.as_retriever(), question_answer_chain)

    user_input = st.chat_input("Type 'Give me a quiz question' or ask about a topic...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            # Pass the user query to the new chain format
            response = qa_chain.invoke({"input": user_input})
            st.write(response["answer"])
