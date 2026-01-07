import streamlit as st
from utils.pdf_loader import load_and_split_pdf
from utils.qa_chain import answer_question, make_qa_chain

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PDF Q&A Assistant",
    page_icon="📄",
    layout="wide",
)

# ---------- INITIALIZE SESSION STATE ----------
if "docs" not in st.session_state:
    st.session_state.docs = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "history" not in st.session_state:
    st.session_state.history = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# ---------- THEME & STYLES (DARK / LIGHT) ----------

compact_mode = st.sidebar.checkbox("Compact layout", value=False)
show_file_info = st.sidebar.checkbox("Show file details", value=True)

BASE_BG =  "#ffffff"
BASE_TEXT ="#0b1220"
ACCENT = "#4A90E2"
CARD_BG =  "#f5f7fa"
PAPER_BG =  "#f8fbff"

css = f"""
<style>
:root {{ --accent: {ACCENT}; --bg: {BASE_BG}; --text: {BASE_TEXT}; --card: {CARD_BG}; --paper: {PAPER_BG}; }}
html, body {{ background: var(--bg); color: var(--text); }}
.main-title {{ font-size: 34px; font-weight: 800; color: var(--accent); margin: 0; }}
.subtitle {{ color: rgba(255,255,255,0.75); margin-top: 4px; margin-bottom: 12px; }}
.upload-box {{ padding: 18px; border-radius: 12px; border: 1px dashed var(--accent); background: var(--paper); }}
.answer-box {{ padding: 18px; border-radius: 12px; background: var(--card); border-left: 5px solid var(--accent); }}
.question-input {{ width: 100%; padding: 8px; border-radius: 8px; }}
.small-muted {{ font-size: 13px; color: rgba(255,255,255,0.6); }}
.card {{ padding: 12px; border-radius: 12px; background: var(--card); }}
.history-item {{ padding:10px; border-radius:8px; margin-bottom:8px; background: rgba(255,255,255,0.02); }}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([6, 2])
with col1:
    st.markdown("<h1 class='main-title'>📄 PDF Q&A Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Upload a PDF and ask anything — Fast, free and accurate. (UI only updated)</div>", unsafe_allow_html=True)
with col2:
     unsafe_allow_html=True

st.markdown("<hr style='margin-top:5px;margin-bottom:5px;border:1px solid #e0e0e0'>", unsafe_allow_html=True)

# ---------- LAYOUT: LEFT: FILE / RIGHT: Q&A ----------
left, right = st.columns([3, 5])

with left:
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your PDF here:", type=["pdf"], key="file_uploader")
    if uploaded_file:
        # show quick file info
        st.success("File uploaded")
        if show_file_info:
            st.markdown(f"**Filename:** {uploaded_file.name}")
            try:
                size_kb = round(len(uploaded_file.getvalue()) / 1024)
                st.markdown(f"**Size:** {size_kb} KB")
            except Exception:
                pass
        # Process button separate from upload to keep logic unchanged
        if st.button("Process PDF ", use_container_width=True):
            st.session_state.processing = True
            with st.spinner("📘 Reading and processing your PDF... "):
                docs = load_and_split_pdf(uploaded_file)
                st.session_state.docs = docs
                st.session_state.qa_chain = make_qa_chain()
            st.session_state.processing = False
            st.success("✅ PDF processed successfully! ")
    else:
        st.info("Upload a PDF .")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("\n")

    # --- Clear Button (no advanced box) ---
    if st.button("Clear Q&A History", use_container_width=True):
     st.session_state.history = []
     st.success("History cleared")

    st.markdown("\n")

    st.markdown("\n")
    if st.session_state.history:
        st.markdown("### 🔁 Recent Questions")
        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            st.markdown(f"<div class='history-item'><b>Q:</b> {item['q']}<br><b>A:</b> {item['a'][:300]}{'...' if len(item['a'])>300 else ''}</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Ask a question about your PDF:")

    # keep the logic unchanged: use the same text_input and answer_question signature
    question = st.text_input("Type your question and press Enter:", key="user_question")

    col_action1, col_action2 = st.columns([3, 1])
    with col_action1:
        ask_button = st.button("Ask", use_container_width=True)
    with col_action2:
        download_history = st.download_button("Download transcript", data='\n'.join([f"Q: {h['q']}\nA: {h['a']}\n" for h in st.session_state.history]) if st.session_state.history else "", file_name="transcript.txt")

    if (question and ask_button) or (question and st.session_state.processing is False and st.session_state.qa_chain and st.session_state.docs and ask_button):
        if not st.session_state.qa_chain or not st.session_state.docs:
            st.warning("You must upload and process a PDF first. Use the button on the left to process the PDF.")
        else:
            with st.spinner("🧠 Thinking... Generating the best answer..."):
                # original logic preserved
                answer = answer_question(st.session_state.qa_chain, question, context=st.session_state.docs)

            # store history
            st.session_state.history.append({"q": question, "a": answer})

            # display answer
            st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
            st.markdown("### 📝 Answer:")
            st.write(answer)
            st.markdown("</div>", unsafe_allow_html=True)

            # quick actions
            col_copy, col_save = st.columns([1, 1])
            with col_copy:
                if st.button("Copy Answer"):
                    st.write("Tip: Use Ctrl+C to copy the answer.")
            with col_save:
                st.download_button("Save Answer", data=answer, file_name="answer.txt")

    elif question and not ask_button:
        st.info("Type your question and click Ask.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("---")
footer_col1, footer_col2 = st.columns([6, 2])
with footer_col1:
    st.markdown("<div class='small-muted'>Built for fast Q&A over PDFs. Logic preserved — only UI changed.</div>", unsafe_allow_html=True)
with footer_col2:
    st.markdown("<div style='text-align:right' class='small-muted'>v1.1</div>", unsafe_allow_html=True)

# ---------- RESPONSIVE TWEAKS ----------
if compact_mode:
    st.markdown("<style> .main .block-container{ padding: 12px 12px; } </style>", unsafe_allow_html=True)

# End of UI-only script
