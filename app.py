import streamlit as st

from backend.inference import run_inference

st.set_page_config(page_title="Medical Analyzer")

st.title("Offline Medical Record Intelligence")

uploaded_file = st.file_uploader("Upload Medical Record", type=["png", "jpg", "jpeg"])

if uploaded_file is not None and st.button("Analyze"):
    result = run_inference(uploaded_file)
    st.subheader("Result")
    st.write(result)
