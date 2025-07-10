# app.py
import streamlit as st
from extractors import extract_text_from_pptx, load_csv
from agent import build_agent
from dotenv import load_dotenv, find_dotenv
import io
import sys

load_dotenv(find_dotenv(), override=True)

st.set_page_config(page_title="📊 Insight Assistant", page_icon="🤖", layout="wide")
st.title("📊 Insight Assistant")
st.subheader("Personal Agentic Assistant to Answer Questions on Structured and Unstructured Data")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.image("assets/schematic.png")
    ppt_file = st.file_uploader("Upload PowerPoint (.pptx)", type="pptx")
    csv_file = st.file_uploader("Upload CSV Data", type="csv")

with col2:
    question = st.text_input("Ask a question about the slides or data:")

    if ppt_file and csv_file and question:
        with st.spinner("Analyzing your files..."):
            ppt_text = extract_text_from_pptx(ppt_file)
            df = load_csv(csv_file)
            agent = build_agent(ppt_text, df)

            # Capture verbose output
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()

            # Run agent
            response = agent.run(question)

            # Reset stdout
            sys.stdout = old_stdout
            agent_logs = mystdout.getvalue()

            # Display results
            st.success(response)
            with st.expander("🔍 See Agent's Reasoning (Verbose Logs)"):
                st.text(agent_logs)
    else:
        st.info("Please upload both a PowerPoint file and a CSV file, then enter your question.")
