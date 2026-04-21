import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

# --- PAGE CONFIG (must be first Streamlit call) ---
st.set_page_config(
    page_title="ExamForge · AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* Root variables */
:root {
    --bg-primary: #0f1117;
    --bg-secondary: #161b27;
    --bg-card: #1c2333;
    --accent-gold: #d4a843;
    --accent-teal: #3ecfb2;
    --text-primary: #e8e3d9;
    --text-muted: #8b8f9e;
    --border: #2a3045;
    --user-bubble: #1e3a5f;
    --ai-bubble: #1c2333;
    --success: #2ecc71;
    --error: #e74c3c;
}

/* Global reset */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1100px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem;
}

/* Logo / Title */
.app-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent-gold);
    letter-spacing: -0.5px;
    margin-bottom: 0.15rem;
}
.app-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1.5rem;
}

/* Divider */
.divider {
    height: 1px;
    background: var(--border);
    margin: 1.2rem 0;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}
.status-ready {
    background: rgba(46, 204, 113, 0.15);
    color: var(--success);
    border: 1px solid rgba(46, 204, 113, 0.3);
}
.status-idle {
    background: rgba(139, 143, 158, 0.1);
    color: var(--text-muted);
    border: 1px solid var(--border);
}

/* Main header */
.main-header {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
}
.main-header span { color: var(--accent-gold); }
.main-tagline {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

/* Tip cards */
.tip-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin: 1.2rem 0 1.8rem 0;
}
.tip-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    font-size: 0.83rem;
    color: var(--text-muted);
    line-height: 1.5;
}
.tip-card strong {
    display: block;
    color: var(--text-primary);
    margin-bottom: 4px;
    font-size: 0.88rem;
}
.tip-card .tip-icon {
    font-size: 1.2rem;
    margin-bottom: 6px;
    display: block;
}

/* Chat container */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--bg-card);
    border: 1px dashed var(--border);
    border-radius: 10px;
    padding: 0.5rem;
}

/* Buttons */
.stButton > button {
    background: var(--accent-gold) !important;
    color: #0f1117 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 1.2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--accent-gold) !important;
}

/* Inputs */
[data-testid="stChatInput"] textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* Alert / info boxes */
.stAlert {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}

/* Section labels in sidebar */
.sidebar-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin: 1rem 0 0.5rem 0;
    font-weight: 500;
}

.doc-info {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.6rem;
}
.doc-info strong { color: var(--text-primary); }

/* Clear button secondary style */
.clear-btn > button {
    background: transparent !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

# --- LAZY IMPORTS (avoid crashing if packages missing) ---
try:
    from langchain_groq import ChatGroq
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import FastEmbedEmbeddings
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate

    DEPS_OK = True
except ImportError as e:
    DEPS_OK = False
    IMPORT_ERROR = str(e)

# --- SESSION STATE INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "doc_name" not in st.session_state:
    st.session_state.doc_name = None
if "doc_pages" not in st.session_state:
    st.session_state.doc_pages = 0

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-logo">ExamForge</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">AI Study Assistant</div>', unsafe_allow_html=True)

    # Status
    if st.session_state.vectorstore:
        st.markdown('<span class="status-badge status-ready">● Document Ready</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-idle">○ No Document Loaded</span>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">📄 Study Material</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type="pdf",
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.markdown(f"""
        <div class="doc-info">
            <strong>{uploaded_file.name}</strong><br>
            {round(uploaded_file.size / 1024, 1)} KB
        </div>
        """, unsafe_allow_html=True)

    process_btn = st.button("⚡ Process Document")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">⚙️ Model</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "LLM Model",
        ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Doc stats
    if st.session_state.vectorstore and st.session_state.doc_name:
        st.markdown(f"""
        <div class="doc-info">
            <strong>Active Document</strong><br>
            📄 {st.session_state.doc_name}<br>
            📃 {st.session_state.doc_pages} pages indexed
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑 Clear Chat"):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("📤 New Doc"):
                st.session_state.vectorstore = None
                st.session_state.messages = []
                st.session_state.doc_name = None
                st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    groq_key = st.text_input("🔑 Groq API Key", type="password",
                              value=os.getenv("GROQ_API_KEY", ""),
                              help="Get yours at console.groq.com")

# ─── DEPENDENCY CHECK ────────────────────────────────────────────────────────
if not DEPS_OK:
    st.error(f"Missing dependencies: `{IMPORT_ERROR}`")
    st.code("pip install langchain-groq langchain-community langchain-huggingface faiss-cpu pypdf sentence-transformers python-dotenv")
    st.stop()

# ─── PROCESS PDF ─────────────────────────────────────────────────────────────
if uploaded_file and process_btn:
    if not groq_key:
        st.sidebar.error("Please enter your Groq API key.")
    else:
        with st.spinner("📚 Processing your document…"):
            try:
                # Write to temp file safely
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                loader = PyPDFLoader(tmp_path)
                docs = loader.load()

                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.split_documents(docs)

                embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
                vectorstore = FAISS.from_documents(chunks, embeddings)

                st.session_state.vectorstore = vectorstore
                st.session_state.doc_name = uploaded_file.name
                st.session_state.doc_pages = len(docs)
                st.session_state.messages = []  # Reset chat for new doc

                os.unlink(tmp_path)  # Clean up temp file
                st.sidebar.success(f"✅ {len(docs)} pages indexed!")
            except Exception as e:
                st.sidebar.error(f"Error processing PDF: {e}")

# ─── MAIN AREA ───────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">Study Smarter,<br><span>Ace Every Exam.</span></div>', unsafe_allow_html=True)
st.markdown('<div class="main-tagline">Upload a document, then ask questions or request quiz questions.</div>', unsafe_allow_html=True)

# Tip cards (shown when no chat yet)
if not st.session_state.messages:
    st.markdown("""
    <div class="tip-grid">
        <div class="tip-card">
            <span class="tip-icon">💡</span>
            <strong>Generate a Quiz</strong>
            "Give me an MCQ on photosynthesis" — get instant multiple-choice questions from your material.
        </div>
        <div class="tip-card">
            <span class="tip-icon">🔍</span>
            <strong>Deep Dive</strong>
            "Explain the difference between X and Y" — get thorough explanations grounded in your notes.
        </div>
        <div class="tip-card">
            <span class="tip-icon">✅</span>
            <strong>Check Your Answer</strong>
            After an MCQ, just type your answer and get instant feedback with explanations.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── CHAT ────────────────────────────────────────────────────────────────────
if st.session_state.vectorstore:

    # Build chain
    system_prompt = """You are a strict but encouraging Exam Tutor. 
Use the context below to answer the student's question accurately.

- If asked for a question or quiz, generate a well-formatted Multiple Choice Question (MCQ) with 4 options (A–D). Label them clearly.
- If the student answers a question, tell them whether they are correct and explain why using the context.
- If asked to explain a concept, give a clear, concise explanation using the context.
- Always cite which part of the material your answer comes from if possible.
- If the answer is not in the context, say so honestly.

Context:
{context}"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    try:
        llm = ChatGroq(
            model=model_choice,          # FIX: was model_name=
            temperature=0.3,
            api_key=groq_key,
        )
        question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
        qa_chain = create_retrieval_chain(
            st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4}),
            question_answer_chain,
        )
    except Exception as e:
        st.error(f"Failed to initialize model: {e}")
        st.stop()

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question, request a quiz, or type your answer…")

    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    response = qa_chain.invoke({"input": user_input})
                    answer = response["answer"]
                except Exception as e:
                    answer = f"⚠️ Error: {e}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    # Empty state prompt
    st.info("👈 Upload a study PDF in the sidebar and click **Process Document** to get started.")
