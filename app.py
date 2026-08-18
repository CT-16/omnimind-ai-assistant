import streamlit as st
import os
from dotenv import load_dotenv
from ai_engine import AIEngine
from document_processor import DocumentProcessor

# Load environment variables
load_dotenv()

# Page Setup
st.set_page_config(
    page_title="OmniMind AI — Smart Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size:2.2rem; font-weight:700; color:#1E293B; margin-bottom:0px; }
    .sub-header { font-size:1.05rem; color:#64748B; margin-bottom:20px; }
    .stMetric { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "doc_text" not in st.session_state:
    st.session_state.doc_text = None
if "doc_meta" not in st.session_state:
    st.session_state.doc_meta = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bot.png", width=70)
    st.title("OmniMind AI")
    st.caption("Week 1 Internship Project | Innovation Hacks 2026")
    st.divider()

    # API Key Handling
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input("Gemini API Key:", value=env_key, type="password", help="Stored securely via .env file or manually entered here.")
    
    if api_key_input:
        api_key = api_key_input
    else:
        api_key = env_key

    st.divider()
    st.subheader("💡 Features Hub")
    st.markdown("""
    - 📄 **Document Intelligence**
    - 📝 **Executive Summarizer**
    - ❓ **Context-Aware Q&A**
    - ✍️ **Content Generator**
    - 🧠 **Smart Suggestions**
    """)
    st.divider()
    st.info("🔒 Secure Architecture: API keys are handled entirely client-side or through local environment variables.")

# Main Interface Header
st.markdown('<div class="main-header">🤖 OmniMind AI Smart Workstation</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An enterprise-ready AI assistant designed to solve complex productivity & document intelligence workflows.</div>', unsafe_allow_html=True)

# Guard Check for API Key
if not api_key:
    st.warning("⚠️ **API Key Required:** Please configure your `GEMINI_API_KEY` in the `.env` file or paste it in the sidebar to unlock OmniMind AI.")
    st.stop()

# Initialize Engine
try:
    engine = AIEngine(api_key=api_key)
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# Workspace Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Document Intelligence & Summary", 
    "💬 Context Q&A", 
    "✍️ Content Generator", 
    "⚡ Smart Suggestions"
])

# ------------------------------------------------------------------------------
# TAB 1: Document Intelligence & Summarization
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Analyze & Summarize Documents")
    uploaded_file = st.file_uploader("Upload a file (PDF or TXT):", type=["pdf", "txt", "md"])

    if uploaded_file:
        try:
            with st.spinner("Parsing document content..."):
                text, meta = DocumentProcessor.process_file(uploaded_file)
                st.session_state.doc_text = text
                st.session_state.doc_meta = meta
            
            st.success("Document loaded successfully!")
            
            # Display Metadata Cards
            c1, c2, c3 = st.columns(3)
            c1.metric("File Name", meta.get("filename", "N/A"))
            c2.metric("Word Count", f"{meta.get('word_count', 0):,}")
            c3.metric("Size", f"{meta.get('size_kb', 0)} KB")

        except Exception as e:
            st.error(f"Error processing file: {e}")

    # Text Input Backup Option
    raw_input = st.text_area("...or paste text directly below:", height=150, value=st.session_state.doc_text or "")
    if raw_input and not st.session_state.doc_text:
        st.session_state.doc_text = raw_input
        st.session_state.doc_meta = {"filename": "Pasted Text", "word_count": len(raw_input.split()), "size_kb": 0}

    st.divider()
    summary_mode = st.selectbox("Select Summary Format:", ["Executive Brief", "Detailed Breakdown", "Action Items"])
    
    if st.button("Generate Summary", type="primary", use_container_width=True):
        if not st.session_state.doc_text:
            st.error("Please upload a document or paste text first.")
        else:
            with st.spinner("AI is synthesizing key insights..."):
                try:
                    summary = engine.summarize_text(st.session_state.doc_text, mode=summary_mode)
                    st.markdown("### 📊 Generated Summary")
                    st.write(summary)
                    st.download_button("📥 Download Summary (.txt)", data=summary, file_name="omnimind_summary.txt")
                except Exception as e:
                    st.error(f"AI Generation Failed: {e}")

# ------------------------------------------------------------------------------
# TAB 2: Question Answering
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Ask Questions About Your Document")
    if not st.session_state.doc_text:
        st.info("💡 Upload a document in Tab 1 to enable grounded Q&A.")
    else:
        st.caption(f"Currently Querying: **{st.session_state.doc_meta.get('filename', 'Active Document')}**")

    user_query = st.text_input("Enter your question:")
    if st.button("Ask Assistant", type="primary"):
        if not user_query.strip():
            st.warning("Please type a question.")
        else:
            context = st.session_state.doc_text if st.session_state.doc_text else "General Knowledge Query"
            with st.spinner("Searching document & formulating response..."):
                try:
                    answer = engine.answer_question(context, user_query)
                    st.session_state.chat_history.append({"q": user_query, "a": answer})
                except Exception as e:
                    st.error(f"Error: {e}")

    # Display Conversation History
    if st.session_state.chat_history:
        st.divider()
        st.subheader("Discussion Log")
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            st.markdown(f"**Q{len(st.session_state.chat_history)-i}: {chat['q']}**")
            st.info(chat["a"])

# ------------------------------------------------------------------------------
# TAB 3: Content Generator
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("AI Workplace Content Generator")
    col_a, col_b = st.columns(2)
    
    with col_a:
        content_type = st.selectbox("Content Type:", [
            "Professional Email", 
            "Project Proposal Draft", 
            "LinkedIn Post", 
            "Bug Report & Technical Ticket", 
            "Meeting Agenda"
        ])
        tone = st.selectbox("Tone / Style:", ["Professional & Formal", "Persuasive & Executive", "Concise & Direct", "Friendly & Creative"])
    
    with col_b:
        topic = st.text_area("Key Details / Prompt:", placeholder="e.g., Requesting budget approval for an AI automation project...", height=115)

    if st.button("Generate Workplace Content", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter key details or a prompt.")
        else:
            with st.spinner("Drafting custom content..."):
                try:
                    generated_output = engine.generate_content(content_type, topic, tone)
                    st.markdown("### 📝 Generated Draft")
                    st.code(generated_output, language="markdown")
                except Exception as e:
                    st.error(f"Content generation error: {e}")

# ------------------------------------------------------------------------------
# TAB 4: Smart Suggestions
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Proactive AI Insights & Recommendations")
    st.markdown("Analyze current document context to uncover hidden risks, recommendations, and strategic actions.")

    if st.button("Run Smart Analysis", type="primary", use_container_width=True):
        if not st.session_state.doc_text:
            st.error("No active text found. Please upload or paste document text in Tab 1 first.")
        else:
            with st.spinner("Executing deep structural analysis..."):
                try:
                    suggestions = engine.get_smart_suggestions(st.session_state.doc_text)
                    st.markdown("### 💡 Strategic Insights & Recommendations")
                    st.success(suggestions)
                except Exception as e:
                    st.error(f"Analysis error: {e}")