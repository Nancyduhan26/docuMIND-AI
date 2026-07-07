import streamlit as st

from utils.pdf_loader import load_pdf
from utils.text_splitter import create_chunks
from utils.embeddings import get_embeddings
from utils.vector_store import create_vector_store
from utils.retriever import retrieve_chunks
from utils.gemini import ask_gemini

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide"
)


# ---------------- SESSION STATE ----------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "chunks_count" not in st.session_state:
    st.session_state.chunks_count = 0
# ---------------- HEADER ----------------

st.markdown("""
<div style="
background: linear-gradient(90deg,#0B4F9C,#2563EB);
padding:25px;
border-radius:18px;
text-align:center;
color:white;
box-shadow:0px 6px 20px rgba(0,0,0,0.15);
margin-bottom:25px;
">

<h1 style="margin-bottom:8px;">🧠 DocuMind AI</h1>

<h4 style="margin-top:0;">
AI-Powered Document Intelligence System
</h4>

<p>
Upload a PDF, build a knowledge base, and ask intelligent questions using Gemini AI.
</p>

</div>
""", unsafe_allow_html=True)
st.markdown("""
### 👋 Welcome

Upload your PDF, build the knowledge base, and ask intelligent questions powered by Retrieval-Augmented Generation (RAG).

""")


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("📊 Dashboard")

    st.markdown("---")

    if st.session_state.document_ready:
        st.markdown("---")

st.markdown("## 💬 Chat with DocuMind AI")

st.markdown("### 💡 Quick Questions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Summarize"):
        st.session_state.quick_question = "Summarize this document."

with col2:
    if st.button("📝 Key Points"):
        st.session_state.quick_question = "What are the key points in this document?"

with col3:
    if st.button("❓ Generate Questions"):
        st.session_state.quick_question = "Generate important interview or exam questions from this document."

default_question = st.session_state.get("quick_question", "")

question = st.text_input(
    "Ask anything about your document...",
    value=default_question,
    placeholder="Example: Explain Human Computer Interaction"
)

if question:

    with st.spinner("🤖 Thinking..."):

        relevant_chunks = retrieve_chunks(
            st.session_state.vector_store,
            question
        )

        context = "\n\n".join(relevant_chunks)

        answer = ask_gemini(
            context,
            question
        )

    st.markdown("### 👤 You")

    st.info(question)

    st.markdown("### 🤖 DocuMind AI")

    st.markdown("### 📊 Analysis Summary")

    col1, col2 = st.columns(2)

    with col1:
     st.metric(
        "📚 Chunks Retrieved",
        len(relevant_chunks)
    )

    st.metric(
        "🧠 Embedding",
        "Gemini"
    )

    with col2:
     st.metric(
        "⚡ Vector Database",
        "FAISS"
    )

    st.metric(
        "✅ Status",
        "Success"
    )
    st.info("💡 Response generated using retrieved document context.")

    with st.expander("📚 View Retrieved Chunks"):

        for i, chunk in enumerate(relevant_chunks):

            st.markdown(f"### Chunk {i+1}")

            st.write(chunk)

            st.markdown("---")
        else:
         st.warning("🟡 Waiting for PDF")

        st.markdown("---")

        st.subheader("📄 Document")

if st.session_state.file_name != "":
        st.write(st.session_state.file_name)
else:
        st.caption("No file uploaded")

        st.markdown("---")

        st.subheader("📊 Document Analytics")

st.metric(
    "📚 Chunks",
    st.session_state.chunks_count
)

if st.session_state.file_name != "":

    st.metric(
        "📄 Document",
        st.session_state.file_name
    )

st.metric(
    "🧠 Embedding",
    "Gemini"
)

st.metric(
    "⚡ Vector DB",
    "FAISS"
)

st.markdown("---")

st.success("🟢 Gemini Connected")

st.success("🟢 FAISS Ready")

st.success("🟢 Retrieval Active")

st.markdown("---")

st.caption("Developed by")

st.write("**Nancy Duhan**")

st.caption("Version 1.0")
# ---------------- PDF UPLOAD ----------------

st.markdown("## 📄 Upload Your PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    st.session_state.file_name = uploaded_file.name

    if st.button("⚙️ Process Document", use_container_width=True):

        with st.spinner("📚 Reading PDF..."):

            text = load_pdf(uploaded_file)

        with st.spinner("✂️ Creating chunks..."):

            chunks = create_chunks(text)

        with st.spinner("🧠 Creating embeddings..."):

            embedding_model = get_embeddings()

        with st.spinner("💾 Building knowledge base..."):

            vector_store = create_vector_store(
                chunks,
                embedding_model
            )

        st.session_state.vector_store = vector_store
        st.session_state.document_ready = True
        st.session_state.chunks_count = len(chunks)

        st.success("✅ Document processed successfully!")
st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:gray;
font-size:15px;
">

<h4>🧠 DocuMind AI</h4>

<p>AI-Powered Document Intelligence System</p>

<p>
Developed by <b>Nancy Duhan</b>
</p>

<p>
Powered by Gemini • FAISS • Streamlit
</p>

</div>
""", unsafe_allow_html=True)