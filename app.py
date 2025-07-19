import streamlit as st
from utils.pii_detector import regex_pii_check, redact_text
from utils.groq_api import analyze_text_with_groq
import plotly.graph_objects as go
from utils.file_extractor import extract_text_from_file

st.set_page_config(page_title="🔐 AI Privacy Risk Analyzer",page_icon="🔎")

st.title("🔐 AI Privacy Risk Analyzer")

st.write("Upload a document (PDF, DOCX, TXT) or paste text below to detect personal data exposure.")


#uploading file


uploaded_file=st.file_uploader("Upload a file",type=["pdf", "docx", "txt"])
file_text=""


if uploaded_file is not None:
    with st.spinner("Extracting text from file..."):
        file_text=extract_text_from_file(uploaded_file)


#Input text


text=st.text_area("Or paste your text here:",value=file_text,height=300)


#Risk chart


def risk_gauge(risk_level):
    risk_map={"Low":30,"Medium":65,"High":90}
    fig=go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_map.get(risk_level,0),
        gauge={'axis': {'range':[0,100]},
               'bar': {'color':"red" if risk_level=="High" else "orange" if risk_level=="Medium" else "green"},
               'steps': [
                   {'range':[0, 40],'color':"lightgreen"},
                   {'range':[40, 70],'color':"gold"},
                   {'range':[70, 100],'color':"tomato"}]},
        title={'text':f"Risk Level:{risk_level}"}
    ))
    st.plotly_chart(fig,use_container_width=True)

if st.button("Analyze Text"):
    if text.strip():

        #Regex

        with st.spinner("Running regex check..."):
            regex_results=regex_pii_check(text)
        st.subheader("🧾 Regex-Based Detection:")
        if regex_results:
            st.markdown("- "+"\n- ".join(regex_results))
        else:
            st.success("✅ No PII detected by regex.")

        #Analysis using AI

        with st.spinner("Running Groq AI analysis..."):
            ai_result=analyze_text_with_groq(text)
        st.subheader("🤖 Groq AI-Based Analysis:")
        st.write(ai_result)

        #Extracting

        risk_level="Medium"
        if "High" in ai_result:
            risk_level="High"
        elif "Low" in ai_result:
            risk_level="Low"
        risk_gauge(risk_level)

        # Highlighting and redact

        highlighted_text=redact_text(text,highlight=True)
        redacted_text=redact_text(text,highlight=False)

        st.subheader("🔍 Highlighted PII:")
        st.markdown(highlighted_text,unsafe_allow_html=True)

        st.subheader("📥 Download Redacted Text:")
        st.download_button(
            label="Download Redacted Text",
            data=redacted_text,
            file_name="redacted_text.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please enter or upload some text to analyze.")
