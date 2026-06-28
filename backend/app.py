import streamlit as st
from input_processor import process_input
from inference import run_inference
from output_formatter import format_output

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Medical Analyzer", layout="wide")

# ---------------- REMOVE DEFAULT WHITE SPACE ----------------
st.markdown("""
<style>
/* REMOVE WHITE TOP SPACE */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* FULL DARK BACKGROUND */
html, body, [class*="css"] {
    background-color: #0b1220 !important;
    color: white;
}

/* MAIN CARD */
.main-card {
    background: #111827;
    padding: 30px;
    border-radius: 20px;
}

/* TITLE */
.title {
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
}

/* SUBTITLE */
.subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 20px;
}

/* INNER CARD */
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1e293b;
}

/* TEXT AREA */
textarea {
    background-color: #020617 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #22c55e);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    border: none;
}

/* TABS FIX */
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    color: white;
    border-bottom: 2px solid #3b82f6;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MAIN UI ----------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Header
st.markdown('<div class="title">📋 Medical Record <span style="color:#3b82f6">Analyzer</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Extract key insights from medical records using AI</div>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([2,1])

# ---------------- LEFT ----------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])

    with tab1:
        text = st.text_area("Enter medical text", height=180, placeholder="Paste your medical record...")

    with tab2:
        uploaded_file = st.file_uploader("Upload file", type=["pdf","txt","docx"])

    st.write("")
    analyze = st.button("✨ Analyze Record")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT ----------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 💡 What you'll get")
    st.write("✔ Extracted Key Information")
    st.write("✔ Structured Summary")
    st.write("✔ Easy Insights")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROCESS ----------------
if analyze:
    if text.strip() == "":
        st.warning("Please enter medical text")
    else:
        try:
            processed = process_input({"input": text})
            result = run_inference(processed)
            output = format_output(processed, result)

            st.success("✅ Analysis Complete")
            st.json(output)

        except Exception as e:
            st.error(str(e))